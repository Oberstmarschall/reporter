from typing import Protocol, List

class PipelineClient(Protocol):
    """Base client interface"""
    def get_pipeline_statuses(self, per_page: int = 5) -> List[str]:
        ...

    def post_message(self, message: str) -> None:
        ...

    def defined_ci_statuses(self) -> object:
        """Dataclass of CI statuses"""
        ...
