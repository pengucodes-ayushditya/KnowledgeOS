from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.enums import ProcessingStatus
from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class ExtractionJob(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "extraction_jobs"

    document_id: Mapped[str] = mapped_column(
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    status: Mapped[ProcessingStatus] = mapped_column(
        SQLEnum(ProcessingStatus),
        default=ProcessingStatus.PENDING,
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    attempt_number: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    atoms_created: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    relationships_created: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="extraction_jobs",
    )