from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.enums import ProcessingStatus
from app.core.enums import ResourceType
from app.db.base import Base
from app.db.mixins import TimestampMixin
from app.db.mixins import UUIDMixin


class Resource(
    Base,
    UUIDMixin,
    TimestampMixin,
):
    __tablename__ = "resources"

    workspace_id: Mapped[str] = mapped_column(
        ForeignKey("workspaces.id"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    resource_type: Mapped[ResourceType] = mapped_column(
        SQLEnum(ResourceType),
        nullable=False,
    )

    status: Mapped[ProcessingStatus] = mapped_column(
        SQLEnum(ProcessingStatus),
        default=ProcessingStatus.PENDING,
        nullable=False,
    )

    workspace: Mapped["Workspace"] = relationship(
        "Workspace",
        back_populates="resources",
    )

    documents: Mapped[list["Document"]] = relationship(
        "Document",
        back_populates="resource",
        cascade="all, delete-orphan",
    )