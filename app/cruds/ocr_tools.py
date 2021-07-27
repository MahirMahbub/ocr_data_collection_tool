from sqlalchemy.orm import Session

from app.cruds.table_repository import TableRepository
from db import models


class OcrToolCrud(TableRepository):

    def __init__(self, db: Session):
        super().__init__(db=db, entity=models.OcrData)

    def get_by_non_extracted(self):
        return self.db.query(self.entity).filter(self.entity.is_extracted == False).all()
