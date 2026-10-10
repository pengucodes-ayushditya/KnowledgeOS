from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.enums import AtomType
from app.core.enums import Domain
from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class KnowledgeAtom(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "knowledge_atoms"

    __table_args__ = (
        Index(
            "ix_atom_domain_type",
            "domain",
            "atom_type",
        ),
    )

    canonical_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    atom_type: Mapped[AtomType] = mapped_column(
        SQLEnum(AtomType),
        nullable=False,
    )

    domain: Mapped[Domain] = mapped_column(
        SQLEnum(Domain),
        nullable=False,
        index=True,
    )

    subdomain: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    importance: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False,
    )

    difficulty: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=1.0,
        nullable=False,
    )

    aliases: Mapped[list["Alias"]] = relationship(
        "Alias",
        back_populates="atom",
        cascade="all, delete-orphan",
    )

    evidence: Mapped[list["Evidence"]] = relationship(
        "Evidence",
        back_populates="atom",
        cascade="all, delete-orphan",
    )

    outgoing_relationships: Mapped[list["KnowledgeRelationship"]] = relationship(
        "KnowledgeRelationship",
        foreign_keys="KnowledgeRelationship.source_atom_id",
        back_populates="source_atom",
        cascade="all, delete-orphan",
    )

    incoming_relationships: Mapped[list["KnowledgeRelationship"]] = relationship(
        "KnowledgeRelationship",
        foreign_keys="KnowledgeRelationship.target_atom_id",
        back_populates="target_atom",
        cascade="all, delete-orphan",
    )