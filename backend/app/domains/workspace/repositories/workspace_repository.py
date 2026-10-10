from sqlalchemy.orm import Session

from app.domains.workspace.models.workspace import Workspace
from app.shared.repositories.base import BaseRepository


class WorkspaceRepository(BaseRepository[Workspace]):
    """
    Repository for Workspace CRUD operations.
    """

    def __init__(self, session: Session):
        super().__init__(session, Workspace)

    def get_by_name(self, name: str) -> Workspace | None:
        return (
            self.session.query(Workspace)
            .filter(Workspace.name == name)
            .first()
        )