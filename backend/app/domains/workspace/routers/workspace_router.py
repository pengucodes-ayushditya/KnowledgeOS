from fastapi import APIRouter
from fastapi import Depends

from app.api.dependencies import get_workspace_service
from app.domains.workspace.schemas.workspace import (
    WorkspaceCreate,
    WorkspaceResponse,
)
from app.domains.workspace.services.workspace_service import (
    WorkspaceService,
)

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)


@router.post(
    "",
    response_model=WorkspaceResponse,
)
def create_workspace(
    data: WorkspaceCreate,
    service: WorkspaceService = Depends(get_workspace_service),
):
    return service.create_workspace(data)


@router.get(
    "",
    response_model=list[WorkspaceResponse],
)
def list_workspaces(
    service: WorkspaceService = Depends(get_workspace_service),
):
    return service.list_workspaces()
