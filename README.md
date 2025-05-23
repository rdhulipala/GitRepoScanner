# GitRepoScanner
Scans a github api and summarizes the content as stdout as well as into a txt file

# Setup
Clone the Repository

```git clone https://github.com/rdhulipala/GitRepoScanner.git```
```cd GitRepoScanner```

Build Docker Image
```docker build -t git-repo-scanner .```
```docker run --rm git-repo-scanner ```

Run with custom github endpoint
```docker run --rm git-repo-scanner rdhulipala/GitRepoScanner```