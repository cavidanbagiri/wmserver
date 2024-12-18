
from datetime import datetime
from sqlalchemy import DateTime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.setup import Base
from models.group_model import GroupModel

class AreaModel(Base):

    __tablename__ = 'areas'

    id: Mapped[int] = mapped_column(primary_key=True)

    quantity: Mapped[float] = mapped_column()
    serial_number: Mapped[str] = mapped_column()
    material_id: Mapped[str] = mapped_column()
    provide_type: Mapped[str] = mapped_column()
    card_number: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    stock_id: Mapped[int] = mapped_column(ForeignKey('stocks.id'))
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), default=1)

    stock: Mapped['StockModel'] = relationship(back_populates='areas')
    group: Mapped['GroupModel'] = relationship(back_populates='areas')

class UnusableMaterialModel(Base):
    __tablename__ = 'unusable_materials'

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[float] = mapped_column()
    comment: Mapped[str] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    stock_id: Mapped[int] = mapped_column(ForeignKey('stocks.id'))
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), default=1)

    stock: Mapped['StockModel'] = relationship(back_populates='unusables')

class ServiceMaterialModel(Base):
    __tablename__ = 'service_materials'

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[float] = mapped_column()
    comment: Mapped[str] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    stock_id: Mapped[int] = mapped_column(ForeignKey('stocks.id'))
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'), default=1)

    stock: Mapped['StockModel'] = relationship(back_populates='services')

