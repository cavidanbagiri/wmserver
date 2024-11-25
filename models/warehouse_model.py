
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.group_model import GroupModel
from models.project_model import ProjectModel

from db.setup import Base


class WarehouseModel(Base):
    __tablename__ = "warehouse_materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    document: Mapped[str] = mapped_column(nullable=True)
    material_name: Mapped[str] = mapped_column()
    quantity: Mapped[float] = mapped_column()
    leftover: Mapped[float] = mapped_column()
    unit: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column(nullable=True)
    currency: Mapped[str] = mapped_column(nullable=True)
    po: Mapped[str] = mapped_column(nullable=True)
    certificate: Mapped[bool] = mapped_column(default=False)
    passport: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))
    # group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'), nullable=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    ordered_id: Mapped[int] = mapped_column(ForeignKey('ordereds.id'))
    material_code_id: Mapped[int] = mapped_column(ForeignKey('material_codes.id'))
    material_type_id: Mapped[int] = mapped_column(ForeignKey('material_types.id'))
    company_id: Mapped[int] = mapped_column(ForeignKey('companies.id'))


    project: Mapped['ProjectModel'] = relationship(back_populates='warehouse_materials')
    # group: Mapped['GroupModel'] = relationship(back_populates='warehouse_materials')
    created_by: Mapped['UserModel'] = relationship(back_populates='warehouse_materials')
    ordered: Mapped['OrderedModel'] = relationship(back_populates='warehouse_materials')
    material_code: Mapped['MaterialCodeModel'] = relationship(back_populates='warehouse_materials')
    material_type: Mapped['MaterialTypeModel'] = relationship(back_populates='warehouse_materials')
    company: Mapped['CompanyModel'] = relationship(back_populates='warehouse_materials')
    stocks: Mapped[list['StockModel']] = relationship(back_populates='warehouse_materials')

    def __str__(self):
        return f'-> {self.id} {self.material_name} -> {self.quantity}'