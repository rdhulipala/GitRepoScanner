import time
import requests

class RetryHandler:
    def __init__(self, max_retries=5, backoff_factor=2):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def get(self, url):
        retry_count = 0
        while retry_count < self.max_retries:
            try:
                response = requests.get(url)
                print(f"Status code: {response.status_code}")
                if response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 0))
                    wait_time = retry_after or (self.backoff_factor ** retry_count)
                    print(f"Rate limited. Waiting for {wait_time} seconds...")
                    time.sleep(wait_time)
                    retry_count += 1
                    continue

                response.raise_for_status()
                return response  # Successful response
            except requests.exceptions.RequestException as e:
                # Only retry on 429. For other exceptions, print and exit.
                print(f"Request failed: {e}")
                return None

        print("Max retries exceeded. Giving up.")
        return None