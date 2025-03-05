from reporter.clients.base import PipelineClient
from reporter.utils.gif import Gif
from typing import List

class PipelineStatusReporter:
    """
    Reports pipeline statuses by posting comments based on failures.
    """

    def __init__(self, client: PipelineClient, gif: Gif):
        self.client = client
        self.gif = gif

    def report_pipeline_status(self) -> None:
        """Reports the pipeline failure status based on recent runs."""
        statuses = self.client.get_pipeline_statuses(per_page=5)
        message = self._pipeline_message(statuses=statuses)

        self.client.post_message(message=message)

    def _pipeline_message(self, statuses: List) -> str:
        failed_in_raw_count = 3
        message = ""
        print(self.client.defined_ci_statuses().failed)
        print(statuses[:failed_in_raw_count])

        if statuses[:failed_in_raw_count].count(self.client.defined_ci_statuses().failed) >= failed_in_raw_count:
            message = (
                f"![]({self.gif.investigate()}) Pipeline [{self.client.pipeline_id}]({self.client.pipeline_url}) has failed "
                f"*{failed_in_raw_count} times in a row!* It's time to investigate! 🔍"
            )
        elif statuses[0] == self.client.defined_ci_statuses().failed:
            message = (
                f"![]({self.gif.stop()}) *Pipeline failed!* Please review [{self.client.pipeline_id}]({self.client.pipeline_url})."
            )

        return message
