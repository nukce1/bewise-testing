from app.database import Base, created_at, intpk
from sqlalchemy.orm import Mapped, mapped_column


class Application(Base):
    __tablename__ = "Application"

    id: Mapped[intpk]
    user_name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str]
    created_at: Mapped[created_at]
