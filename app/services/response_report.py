from sqlalchemy.orm import Session

from app.cruds.response_report import ResponseReportCrud
from db.schemas import ResponseReportCreate, ResponseReportUpdate


class ResponseReportService(object):
    def create_response_report_by_class_id(self, db: Session, class_id):
        item = ResponseReportCreate(class_id=class_id)
        report_crud_object = ResponseReportCrud(db=db).store(item=item)
        # db.commit()
        return report_crud_object

    def update_response_report(self, db: Session, id_: int, num_character_label):
        item = ResponseReportUpdate(num_character_label=num_character_label)
        if ResponseReportCrud(db=db).update(id_=id_, item=item):
            db.commit()
            return True
        else:
            return False
