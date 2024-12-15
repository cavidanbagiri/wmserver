from datetime import datetime
from typing import Set

from sqlalchemy import DateTime
from sqlalchemy import func

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from db.setup import Base
from models.warehouse_model import WarehouseModel
from models.area_model import AreaModel
# from models.area_model import ServiceMaterialModel
# from models.area_model import UnusableMaterialModel


class StockModel(Base):
    __tablename__ = 'stocks'

    id: Mapped[int] = mapped_column(primary_key=True)

    quantity: Mapped[float] = mapped_column()
    leftover: Mapped[float] = mapped_column()

    serial_number: Mapped[str] = mapped_column()
    material_id: Mapped[str] = mapped_column()

    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouse_materials.id'))

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    warehouse_materials: Mapped['WarehouseModel'] = relationship(back_populates='stocks')

    areas: Mapped[Set['AreaModel']] = relationship(back_populates='stock')
    unusables: Mapped[Set['UnusableMaterialModel']] = relationship(back_populates='stock')
    services: Mapped[list['ServiceMaterialModel']] = relationship(back_populates='stock')

    def __str__(self):
        return f'id-> {self.id} | quantity-> {self.quantity} | leftover-> {self.leftover} '

