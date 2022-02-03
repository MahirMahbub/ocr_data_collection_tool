from sqlalchemy import func
from sqlalchemy.orm import Session

from app.cruds.table_repository import TableRepository
from db import models


class ClassLabelCrud(TableRepository):

    def __init__(self, db: Session):
        super().__init__(db=db, entity=models.ClassLabel)

    def store(self, item, checker=None):
        item = item.dict(exclude_unset=True)
        exist = False
        if checker:
            exist = self.db.query(self.entity).filter_by(**checker).first()
        if not exist:
            ocr_model_object = self.entity(**item)
            self.db.add(ocr_model_object)
            return ocr_model_object

    def get_by_round_robin(self):
        sub_query = self.db.query(func.min(self.entity.round_robin_marker))
        class_label_instance = self.db.query(self.entity).filter(self.entity.round_robin_marker == sub_query).first()
        class_label_instance.round_robin_marker += 1

        return class_label_instance
