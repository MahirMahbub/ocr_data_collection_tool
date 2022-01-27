from sqlalchemy.orm import Session

from app.cruds.table_repository import TableRepository
from db import models


class CharacterCrud(TableRepository):

    def __init__(self, db: Session):
        super().__init__(db=db, entity=models.Characters)

    def store(self, item, checker=None):
        item = item.dict(exclude_unset=True)
        exist = False
        if checker:
            exist = self.db.query(self.entity).filter_by(**checker).first()
        if not exist:
            ocr_model_object = self.entity(**item)
            self.db.add(ocr_model_object)
            return ocr_model_object

    def get_images(self, limit=5):
        return self.db.query(self.entity).filter(self.entity.is_labeled == False,
                                                 self.entity.class_id == None).limit(limit).all()

    def get_by_class_id(self, class_id: str):
        return self.db.query(self.entity).filter(self.entity.class_id == class_id).all()

    def get_id_by_path(self, path):
        return self.db.query(self.entity.id).filter(self.entity.character_path == path).first()
