from sqlalchemy.orm import Session

from app.domains.workspace.models.workspace import Workspace
from app.domains.workspace.repositories.workspace_repository import (
    WorkspaceRepository,
)
from app.domains.workspace.schemas.workspace import WorkspaceCreate
from app.shared.services.base import BaseService


class WorkspaceService(BaseService):
    """
    Business logic for workspaces.
    """

    def __init__(self, session: Session):
        super().__init__(session)
        self.repository = WorkspaceRepository(session)

    def create_workspace(self, data: WorkspaceCreate) -> Workspace:
        try:
            workspace = self.repository.create(
                name=data.name,
                description=data.description,
            )
            self.session.commit()
            return workspace
        except Exception:
            self.session.rollback()
            raise

    def get_workspace(self, workspace_id: str) -> Workspace | None:
        return self.repository.get(workspace_id)

    def list_workspaces(self) -> list[Workspace]:
        return self.repository.list()

    def delete_workspace(self, workspace: Workspace):
        self.repository.delete(workspace)
