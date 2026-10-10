from sqlalchemy.orm import Session

from app.domains.knowledge.models.evidence import Evidence
from app.shared.repositories.base import BaseRepository


class EvidenceRepository(BaseRepository[Evidence]):

    def __init__(self, session: Session):
        super().__init__(session, Evidence)