from sqlalchemy.orm import Session

from app.domains.knowledge.models.atom import KnowledgeAtom
from app.shared.repositories.base import BaseRepository


class KnowledgeAtomRepository(BaseRepository[KnowledgeAtom]):

    def __init__(self, session: Session):
        super().__init__(session, KnowledgeAtom)