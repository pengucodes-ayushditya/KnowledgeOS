from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.enums import RelationshipType
from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class KnowledgeRelationship(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    """
    Directed edge between two KnowledgeAtoms.

    Examples:

        Article 32 ----PROTECTS----> Fundamental Rights

        Finance Commission ----RECOMMENDS----> Tax Devolution

        Basic Structure Doctrine ----LIMITS----> Parliament
    """

    __tablename__ = "knowledge_relationships"

    __table_args__ = (
        UniqueConstraint(
            "source_atom_id",
            "target_atom_id",
            "relationship_type",
            name="uq_knowledge_relationship",
        ),
    )

    source_atom_id: Mapped[str] = mapped_column(
        ForeignKey(
            "knowledge_atoms.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    target_atom_id: Mapped[str] = mapped_column(
        ForeignKey(
            "knowledge_atoms.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    relationship_type: Mapped[RelationshipType] = mapped_column(
        SQLEnum(RelationshipType),
        nullable=False,
    )

    weight: Mapped[float] = mapped_column(
        Float,
        default=1.0,
        nullable=False,
    )

    source_atom: Mapped["KnowledgeAtom"] = relationship(
        "KnowledgeAtom",
        foreign_keys=[source_atom_id],
        back_populates="outgoing_relationships",
    )

    target_atom: Mapped["KnowledgeAtom"] = relationship(
        "KnowledgeAtom",
        foreign_keys=[target_atom_id],
        back_populates="incoming_relationships",
    )