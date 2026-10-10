from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

# Workspace
from app.domains.workspace.repositories.workspace_repository import (
    WorkspaceRepository,
)
from app.domains.workspace.services.workspace_service import WorkspaceService


def get_workspace_repository(
    db: Session = Depends(get_db),
) -> WorkspaceRepository:
    return WorkspaceRepository(db)


def get_workspace_service(
    db: Session = Depends(get_db),
) -> WorkspaceService:
    return WorkspaceService(db)
