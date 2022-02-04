from typing import List

from fastapi import Depends, HTTPException, status, UploadFile, File, Query, Path, Body
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, FileResponse

from app.cruds.class_label import ClassLabelCrud
from app.depends.db_depend import get_db
from app.services.ocr import Ocr as ServiceOcr
from db.schemas import CharacterClassUpdate

router = InferringRouter()


@cbv(router)
class Ocr:
    db: Session = Depends(get_db)

    @router.post("/data/images/")
    def store_ocr_images_collection(self, files: List[UploadFile] = File(None)):
        ocr_service_object = ServiceOcr()
        failed_upload_list, success_upload_list, error = ocr_service_object.ocr_data_file_upload(self.db, files)
        if not success_upload_list:
            return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                 detail="Any Image not uploaded")
        else:
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={
                "succeedUploadList": success_upload_list,
                "failedUploadList": failed_upload_list,
                "error": error
            })

    @router.get("/data/images/")
    def get_ocr_images_collection(self):
        datum = ServiceOcr().get_ocr_data(self.db)
        response_list = []
        for data in datum:
            response_list.append({
                "id": data.id,
                "isExtracted": data.is_extracted,
                "details": "/data/image/?id_={}".format(data.id)
            })
        return response_list

    @router.get("/data/image/")
    def get_ocr_image(self, id_: int = Query(default=None)):
        if id_ is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail="Any Image not found")
        else:
            data = ServiceOcr().get_ocr_data_by_id(self.db, id_)
            return {
                "id": data.id,
                "isExtracted": data.is_extracted,
                "image": "/data/image/response/?id_={}".format(data.id)
            }

    @router.get("/data/image/response/")
    def get_ocr_main_image_response(self, id_: int = Query(default=None)):
        if id_ is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail="Any Image not found")
        else:
            data = ServiceOcr().get_ocr_data_by_id(self.db, id_)
            return FileResponse(data.file_path)

    @router.get("/classification/images/")
    def get_class_and_data_to_classify(self, limit: int = Query(5)):
        unclassified_images, class_label_object = ServiceOcr().\
            get_character_images_and_class_to_be_classify(self.db,limit=limit)
        response_list = []
        for data in unclassified_images:
            response_list.append({
                "id": data.id,
                "url": "/classification/image/response/?id_={}".format(data.id),
            })
        return {
            "classToBeLabeled": class_label_object.class_id,
            "images": response_list
        }

    @router.get("/classification/image/response/")
    def get_ocr_image_response(self, id_: int = Query(default=None)):
        if id_ is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail="Any Image not found")
        else:
            data = ServiceOcr().get_character_image_by_id(self.db, id_)
            print(data)
            return FileResponse(data.character_path)

    @router.patch("/classification/image/{id_}", status_code=201)
    def update_character_image_class(self, id_: int = Path(default=None), body: CharacterClassUpdate = Body(...)):
        if id_ is None:
            return HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                 detail="Provide a valid id")
        else:

            if ServiceOcr().update_character_image_class(self.db, id_, body):
                return HTTPException(status_code=status.HTTP_201_CREATED,
                                     detail="Character image updated")

    @router.get("/data/class/image/")
    def get_class_label_images(self, class_id: int = Query(None)):
        if class_id is None:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                 detail="Any Image not found")
        else:
            ids = ServiceOcr().get_images_for_class_label(self.db, class_id)
            response_list = []
            for id_ in ids:
                response_list.append({
                    "id": id_[0],
                    "url": "/classification/image/response/?id_={}".format(id_[0]),
                })
            return response_list
