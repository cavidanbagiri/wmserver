
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.setup import Base

class MaterialCodeModel(Base):
    __tablename__ = "material_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    material_code: Mapped[str] = mapped_column()
    material_description: Mapped[str] = mapped_column()

    warehouse_materials: Mapped[list['WarehouseModel']] = relationship(back_populates='material_code')

