from sqlalchemy.orm import Session

from app.domains.ingestion.models.resource import Resource
from app.shared.repositories.base import BaseRepository


class ResourceRepository(BaseRepository[Resource]):

    def __init__(self, session: Session):
        super().__init__(session, Resource)