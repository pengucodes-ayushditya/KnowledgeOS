from sqlalchemy.orm import Session

from app.domains.ingestion.models.extraction_job import ExtractionJob
from app.shared.repositories.base import BaseRepository


class ExtractionJobRepository(BaseRepository[ExtractionJob]):

    def __init__(self, session: Session):
        super().__init__(session, ExtractionJob)