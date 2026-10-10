from sqlalchemy.orm import Session

from app.domains.ingestion.models.embedding import Embedding
from app.shared.repositories.base import BaseRepository


class EmbeddingRepository(BaseRepository[Embedding]):

    def __init__(self, session: Session):
        super().__init__(session, Embedding)