
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.setup import Base

class MaterialTypeModel(Base):
    __tablename__ = 'material_types'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()

    warehouse_materials: Mapped[list['WarehouseModel']] = relationship(back_populates='material_type')

