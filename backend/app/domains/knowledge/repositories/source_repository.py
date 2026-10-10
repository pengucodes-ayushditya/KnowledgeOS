from sqlalchemy.orm import Session

from app.domains.knowledge.models.source import Source
from app.shared.repositories.base import BaseRepository


class SourceRepository(BaseRepository[Source]):

    def __init__(self, session: Session):
        super().__init__(session, Source)