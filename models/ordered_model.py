
from db.setup import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.hybrid import hybrid_property

class OrderedModel(Base):
    __tablename__ = 'ordereds'

    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()

    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id'))
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))

    
    group: Mapped['GroupModel'] = relationship(back_populates='ordereds')
    project: Mapped['ProjectModel'] = relationship(back_populates='ordereds')

    warehouse_materials: Mapped[list['WarehouseModel']] = relationship(back_populates='ordered')

    @hybrid_property
    def username(self):
        return f'{self.first_name.title()} {self.last_name.title()}'

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.group}'

