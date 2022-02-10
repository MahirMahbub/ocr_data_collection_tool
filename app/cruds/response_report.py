from sqlalchemy.orm import Session

from app.cruds.table_repository import TableRepository
from app.utils import overrides
from db import models


class ResponseReportCrud(TableRepository):

    def __init__(self, db: Session):
        super().__init__(db=db, entity=models.ResponseReport)

    @overrides(TableRepository)
    def store(self, item, checker=None):
        model_object  =None
        item = item.dict(exclude_unset=True)
        exist = False
        if checker:
            exist = self.db.query(self.entity).filter_by(**checker).first()
        if not exist:
            model_object = self.entity(**item)
        self.db.add(model_object)
        self.db.flush()
        # self.db.refresh(model_object)
        return model_object