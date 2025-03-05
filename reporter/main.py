import os
from reporter.clients.gitlab import GitLabMrPipelineClient
from reporter.reporters.pipeline_status import PipelineStatusReporter
from reporter.utils.gif import Gif


if __name__ == "__main__":
    gitlab_client = GitLabMrPipelineClient(
        api_url=os.environ['CI_API_V4_URL'],
        api_token=os.environ['GITLAB_API_TOKEN'],
    )

    reporter = PipelineStatusReporter(
        client=gitlab_client,
        gif=Gif(repo_url="https://raw.githubusercontent.com/Oberstmarschall/reporter/refs/heads/master"),
    )

    reporter.report_pipeline_status()
