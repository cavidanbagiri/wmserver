import datetime

from sqlalchemy import ForeignKey, DateTime, func, null
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from db.setup import Base
from models.group_model import GroupModel
from models.user_status_models import UserStatusModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    image_url: Mapped[str] = mapped_column(nullable=True)

    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=True)
    user_status_id: Mapped[int] = mapped_column(ForeignKey('user_status_models.id'))

    warehouse_materials: Mapped[list['WarehouseModel']] = relationship(back_populates='created_by')
    user_status: Mapped['UserStatusModel'] = relationship(back_populates='users')
    group: Mapped['GroupModel'] = relationship(back_populates='users')


    @hybrid_property
    def username(self):
        return f"{self.first_name} {self.last_name}"

    @hybrid_property
    def status_name(self):
        return f"{self.user_status.status_name}"

    def __str__(self):
        return self.email


    def dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'username': self.username,
        }

