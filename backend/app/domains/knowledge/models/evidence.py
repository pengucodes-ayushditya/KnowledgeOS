from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class Evidence(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    """
    Connects a KnowledgeAtom to the exact supporting span
    inside a Chunk together with its canonical Source.
    """

    __tablename__ = "evidence"

    __table_args__ = (
        UniqueConstraint(
            "atom_id",
            "chunk_id",
            "start_offset",
            "end_offset",
            name="uq_evidence_span",
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

    chunk_id: Mapped[str] = mapped_column(
        ForeignKey(
            "chunks.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    source_id: Mapped[str | None] = mapped_column(
        ForeignKey(
            "sources.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    start_offset: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    end_offset: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=1.0,
        nullable=False,
    )

    created_by: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    atom: Mapped["KnowledgeAtom"] = relationship(
        "KnowledgeAtom",
        back_populates="evidence",
    )

    chunk: Mapped["Chunk"] = relationship(
        "Chunk",
        back_populates="evidence",
    )

    source: Mapped["Source | None"] = relationship(
        "Source",
        back_populates="evidence",
    )