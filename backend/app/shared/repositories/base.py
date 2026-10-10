from __future__ import annotations

from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Generic repository providing reusable CRUD operations.
    """

    def __init__(
        self,
        session: Session,
        model: Type[ModelType],
    ):
        self.session = session
        self.model = model

    def create(self, **kwargs: Any) -> ModelType:
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.flush()
        self.session.refresh(instance)
        return instance

    def get(self, object_id: Any) -> Optional[ModelType]:
        return self.session.get(self.model, object_id)

    def list(self) -> list[ModelType]:
        return list(
            self.session.scalars(
                select(self.model)
            ).all()
        )

    def delete(self, instance: ModelType) -> None:
        self.session.delete(instance)

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def flush(self) -> None:
        self.session.flush()