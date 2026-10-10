from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class Source(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    """
    Canonical source of knowledge.

    Examples:
        - NCERT Class XI Polity
        - Laxmikant 7th Edition
        - PIB
        - PRS India
        - Constitution of India
    """

    __tablename__ = "sources"

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )

    author: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    publisher: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    source_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    edition: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    evidence: Mapped[list["Evidence"]] = relationship(
        "Evidence",
        back_populates="source",
    )