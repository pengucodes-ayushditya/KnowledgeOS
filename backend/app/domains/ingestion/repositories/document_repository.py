from sqlalchemy.orm import Session

from app.domains.ingestion.models.document import Document
from app.shared.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):

    def __init__(self, session: Session):
        super().__init__(session, Document)