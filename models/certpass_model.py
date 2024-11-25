from tkinter.tix import COLUMN

from sqlalchemy import Table, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from db.setup import Base

class  CertPassModels(Base):
    __tablename__ = 'certpass_models'

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column()
    file_name: Mapped[str] = mapped_column()
    warehouse_id: Mapped[int] = mapped_column(ForeignKey('warehouse_materials.id'))

    def __str__(self):
        return f'{self.warehouse_id} -> {self.link}'

