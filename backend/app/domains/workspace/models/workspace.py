from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class Workspace(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    """
    Root entity.

    Every uploaded resource belongs to exactly one workspace.
    """

    __tablename__ = "workspaces"

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        String(1000),
        nullable=True,
    )

    resources: Mapped[list["Resource"]] = relationship(
        "Resource",
        back_populates="workspace",
        cascade="all, delete-orphan",
    )