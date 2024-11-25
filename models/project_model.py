
from sqlalchemy.orm import relationship

from sqlalchemy.orm import Mapped, mapped_column

from db.setup import Base

class ProjectModel(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)

    project_name: Mapped[str] = mapped_column()
    project_code: Mapped[str] = mapped_column()


    ordereds: Mapped[list['OrderedModel']] = relationship(back_populates='project')

    warehouse_materials: Mapped[list['WarehouseModel']] = relationship(back_populates='project')


