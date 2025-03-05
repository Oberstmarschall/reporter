class Gif:
    """Urls to gifs"""

    def __init__(self, repo_url: str):
        self.web_sources = f"{repo_url}/reporter/sources"

    def investigate(self) -> str:
        return f"{self.web_sources}/investigate.gif"

    def stop(self) -> str:
        return f"{self.web_sources}/stop.gif"
