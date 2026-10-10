from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class Alias(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    """
    Alternative names for a KnowledgeAtom.

    Examples:

    KnowledgeAtom:
        Fundamental Rights

    Aliases:
        FR
        Part III
        Fundamental Right
    """

    __tablename__ = "aliases"

    __table_args__ = (
        UniqueConstraint(
            "atom_id",
            "alias",
            name="uq_atom_alias",
        ),
    )

    atom_id: Mapped[str] = mapped_column(
        ForeignKey(
            "knowledge_atoms.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    alias: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    atom: Mapped["KnowledgeAtom"] = relationship(
        "KnowledgeAtom",
        back_populates="aliases",
    )