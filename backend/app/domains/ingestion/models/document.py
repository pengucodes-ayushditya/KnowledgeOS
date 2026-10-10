from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class Document(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    """
    Represents a physical document associated with a Resource.

    Examples:
        - Constitution.pdf
        - Laxmikant 7th Edition.pdf
        - NCERT History Class 12.pdf
    """

    __tablename__ = "documents"

    resource_id: Mapped[str] = mapped_column(
        ForeignKey(
            "resources.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    checksum: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        unique=True,
        index=True,
    )

    page_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    language: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    metadata_json: Mapped[dict[str, object] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    resource: Mapped["Resource"] = relationship(
        "Resource",
        back_populates="documents",
    )

    chunks: Mapped[list["Chunk"]] = relationship(
        "Chunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    extraction_jobs: Mapped[list["ExtractionJob"]] = relationship(
        "ExtractionJob",
        back_populates="document",
        cascade="all, delete-orphan",
    )