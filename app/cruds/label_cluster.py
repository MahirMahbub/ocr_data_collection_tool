from sqlalchemy.orm import Session

from app.cruds.table_repository import TableRepository
from db import models


class LabelClusterCrud(TableRepository):

    def __init__(self, db: Session):
        super().__init__(db=db, entity=models.LabelCluster)

    def get_by_class_id(self, class_id: int):
        return self.db.query(self.entity).filter(self.entity.class_id == class_id).first()
