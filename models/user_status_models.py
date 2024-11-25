
# from sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship


from db.setup import Base

class UserStatusModel(Base):
    __tablename__ = "user_status_models"

    id: Mapped[int] = mapped_column(primary_key=True)

    status_name: Mapped[str] = mapped_column()
    status_code: Mapped[str] = mapped_column()

    users: Mapped[list["UserModel"]] = relationship(back_populates="user_status")
