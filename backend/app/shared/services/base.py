from sqlalchemy.orm import Session


class BaseService:
    """
    Base class for all domain services.
    """

    def __init__(self, session: Session):
        self.session = session