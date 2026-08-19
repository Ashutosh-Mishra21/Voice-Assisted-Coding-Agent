from pathlib import Path


class RepositoryScanner:

    SUPPORTED_EXTENSIONS = {
        ".py",
        ".java",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".html",
        ".css",
        ".scss",
        ".md",
    }

    def scan(self, repository_path: str):

        repository = Path(repository_path)

        files = []

        for extension in self.SUPPORTED_EXTENSIONS:
            files.extend(repository.rglob(f"*{extension}"))

        return sorted(files)
