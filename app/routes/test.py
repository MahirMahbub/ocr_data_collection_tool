import os

from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session


from app.depends.db_depend import get_db

from db import models

router = InferringRouter()


@cbv(router)
class Test:
    db: Session = Depends(get_db)

    @router.get("/")
    def get(self):
        preload_flag = self.db.query(models.Properties).filter(models.Properties.name == "CharacterDataPreLoad").first()
        print(preload_flag)
        if not preload_flag:
            current_path = os.getcwd()
            class_data_path = "/app/data/training_set/"
            list_dir = os.listdir(current_path + class_data_path)
            for class_name in list_dir:
                list_of_files = [current_path + class_data_path + os.path.join(class_name, f) for f in
                                 os.listdir(current_path + class_data_path + class_name+"/")]
                print(list_of_files)
                # print(current_path + class_data_path + class_name)
        # ocr_processing_object = OcrCharacterSeperator()
        # print(os.getcwd())
        # images_and_save_path = ocr_processing_object.character_extractor(os.getcwd()+r"/app/Screenshot 2021-07-24 141745.png")
        # for save_path, char_img in images_and_save_path:
        #     imageio.imwrite(save_path, char_img)
        #     character_model_object = models.Characters(character_path=save_path)
        #     self.db.add(character_model_object)
        # try:
        #     self.db.commit()
        #     raise HTTPException(status_code=status.HTTP_201_CREATED,
        #                         detail="Character extracted from image")
        # except Exception as e:
        #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
        #                         detail="Character can not be extracted from image")

    # def update(self):
    #     from db.schemas import OcrDataUpdate
    #     item = OcrDataUpdate(is_extracted=True)
    #     OcrToolCrud.update(item=item, id_=ocr_image.id)
    #     self.db.commit()
    #
    @router.get("/test/")
    def get_test(self):
        from app.custom_classes.image_clustering import ImageClustering
        print(ImageClustering(db=self.db, class_id=23).apply_kmean())



