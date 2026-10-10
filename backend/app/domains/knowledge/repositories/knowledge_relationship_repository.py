from sqlalchemy.orm import Session

from app.domains.knowledge.models.relationship import KnowledgeRelationship
from app.shared.repositories.base import BaseRepository


class KnowledgeRelationshipRepository(
    BaseRepository[KnowledgeRelationship]
):

    def __init__(self, session: Session):
        super().__init__(session, KnowledgeRelationship)