
from db.setup import Base

from sqlalchemy.orm import mapped_column, Mapped, relationship

class GroupModel(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column()

    ordereds: Mapped[list['OrderedModel']] = relationship(back_populates='group')

    users: Mapped[list["UserModel"]] = relationship(back_populates="group")
