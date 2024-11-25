
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from db.setup import Base

class CompanyModel(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)

    company_name: Mapped[str] = mapped_column()
    country: Mapped[str] = mapped_column()
    email_address: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    warehouse_materials: Mapped[list['WarehouseModel']] = relationship(back_populates='company')


