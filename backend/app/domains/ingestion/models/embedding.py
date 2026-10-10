from pgvector.sqlalchemy import Vector

from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.constants import DEFAULT_EMBEDDING_DIMENSION
from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class Embedding(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    """
    Stores the vector embedding for exactly one Chunk.
    """

    __tablename__ = "embeddings"

    chunk_id: Mapped[str] = mapped_column(
        ForeignKey(
            "chunks.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    dimension: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    vector: Mapped[Vector] = mapped_column(
        Vector(DEFAULT_EMBEDDING_DIMENSION),
        nullable=False,
    )

    chunk: Mapped["Chunk"] = relationship(
        "Chunk",
        back_populates="embedding",
    )