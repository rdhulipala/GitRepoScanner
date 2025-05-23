from src.retry_handler import RetryHandler
import sys


class GitRepoScanner:
    BASE_URL = 'https://api.github.com/repos'

    def __init__(self,repo_full_name):
        self.retry_handler = RetryHandler()
        self.repo_full_name = repo_full_name
        self.endpoint = f"{self.BASE_URL}/{self.repo_full_name}"

    def fetch_github_data(self):
        try:
            response = self.retry_handler.get(self.endpoint)
            response.raise_for_status()
            content_type = response.headers.get('Content-Type')
            if content_type in content_type.lower():
                data = response.json()
                return data

            print(f"Response is not in JSON format. format is {response.headers.get('Content-Type')}")
            return None
        except:
            print(f"encountered an error while parsing the repo_full_name: {self.repo_full_name}")
            return None

    def print_data(self, data,indent=0):
        for key, value in data.items():
            if isinstance(value, dict):
                print("  " * indent + f"{key}:")
                self.print_data(value, indent + 2)
            else:
                print("  " * indent + f"{key}: {value}")

    def print_data_to_file(self, data, file_name):
        with open(file_name,'w') as f:
            for key, value in data.items():
                f.write(f"{key}: {value}\n")

    def summarize_data(self, data):
        if not data:
            print("No data returned")
        else:
            try:
                print("###################### Repo Summary ##################")
                print(f"Name: {data['name']}")
                print(f"Description: {data['description']}")
                print(f"URL: {data['url']}")
                print(f"This page has a total of {len(data)} fields")
                parent_keys_with_children = [k for k, v in data.items() if isinstance(v, dict)]
                print("Parent fields containing sub fields", parent_keys_with_children)
                print("###################### Repo Details ##################")
                self.print_data(data,0)
                print("##########################################################")
                file_name=data['owner']['login']+"_"+data['name']+".txt"
                self.print_data_to_file(data,file_name)
            except:
                print("encountered an error while parsing the data returned")

    def get_followers(self, data):
        if not data:
            print("No data returned")
            return None

        followers_url = data.get('owner').get('followers_url')
        if not followers_url:
            print("No followers URL found")
            return []
        follower_ids = []
        page = 1
        per_page = 100
        while True:
            url = f"{followers_url}?per_page={per_page}&page={page}"
            response = self.retry_handler.get(url)
            if response is None:
                break  # Exceeded retries or unrecoverable error

            page_data = response.json()

            if not page_data:
                break

            follower_ids.extend(follower['id'] for follower in page_data)
            page += 1

            data = response.json()

            # Stop when no more followers are returned
            if not data:
                break

            # Extract follower IDs
            for follower in data:
                follower_ids.append(follower['id'])

            page += 1

        return follower_ids



if __name__ == "__main__":
    repo_full_name = sys.argv[1]
    helper = GitRepoScanner(repo_full_name)
    data = helper.fetch_github_data()
    helper.summarize_data(data)

