from sqlalchemy.orm import Session

from app.domains.ingestion.models.chunk import Chunk
from app.shared.repositories.base import BaseRepository


class ChunkRepository(BaseRepository[Chunk]):

    def __init__(self, session: Session):
        super().__init__(session, Chunk)