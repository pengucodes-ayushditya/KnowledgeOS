from sqlalchemy.orm import Session

from app.domains.knowledge.models.alias import Alias
from app.shared.repositories.base import BaseRepository


class AliasRepository(BaseRepository[Alias]):

    def __init__(self, session: Session):
        super().__init__(session, Alias)