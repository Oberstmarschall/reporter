import requests
from os import getenv
from reporter.clients.base import PipelineClient
from typing import List
from dataclasses import dataclass


class GitLabMrPipelineClient(PipelineClient):
    """
    A client for interacting with the GitLab API, for fetching merge request pipeline statuses and posting comments.
    """

    def __init__(
        self,
        api_url: str,
        api_token: str,
    ):
        self.api_url = api_url
        self.api_token = api_token
        self.headers = {
            "PRIVATE-TOKEN": self.api_token,
            "Content-Type": "application/json",
        }

    @property
    def pipeline_id(self) -> str:
        return getenv("CI_PIPELINE_IID", "unknown")

    @property
    def pipeline_url(self) -> str:
        return getenv("CI_PIPELINE_URL", "unknown")

    @property
    def merge_request_id(self) -> str:
        return getenv("CI_MERGE_REQUEST_IID", "unknown")

    @property
    def project_id(self) -> str:
        return getenv("CI_PROJECT_ID", "unknown")

    def defined_ci_statuses(self) -> object:
        return GitLabPipelineStatuses

    def get_pipeline_statuses(self, per_page: int = 5) -> List[str]:
        """Fetches the statuses of the latest pipelines associated with the merge request."""
        url = (
            f"{self.api_url}/projects/{self.project_id}/merge_requests/{self.merge_request_id}/pipelines"
            f"?per_page={per_page}"
        )
        response = requests.get(url, headers=self.headers)


        if response.status_code != 200:
            raise RuntimeError(f"Error fetching pipelines: {response.status_code}, {response.text}")

        return [pipeline["status"] for pipeline in response.json()]

    def post_message(self, message: str) -> None:
        """Posts a message as a comment on the merge request."""
        url = f"{self.api_url}/projects/{self.project_id}/merge_requests/{self.merge_request_id}/notes"
        payload = {"body": message}

        print(payload)
        response = requests.post(url, json=payload, headers=self.headers)

        if response.status_code != 201:
            raise RuntimeError(f"Error posting message: {response.status_code}, {response.text}")


@dataclass(frozen=True)
class GitLabPipelineStatuses():
    failed = "failed"
    success = "success"
