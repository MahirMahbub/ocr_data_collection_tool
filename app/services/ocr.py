from skimage import io
import os
from pathlib import Path
from typing import List, Tuple

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.cruds.character import CharacterCrud
from app.cruds.class_label import ClassLabelCrud
from app.cruds.ocr_tools import OcrToolCrud
from app.custom_classes.file_path import next_file_name
from custom_classes.image_clustering import ImageClustering
from db import models
from db.schemas import OcrDataCreate, CharacterUpdate, CharacterClassUpdate
from skimage.metrics import structural_similarity as ssim

image_file_extensions = IMAGE = ('ras', 'xwd', 'bmp', 'jpe', 'jpg', 'jpeg', 'xpm', 'ief', 'pbm', 'tif', 'gif', 'ppm',
                                 'xbm', 'tiff', 'rgb', 'pgm', 'png', 'pnm')


class Ocr(object):

    def ocr_data_file_upload(self, db: Session, files: List[UploadFile]) -> Tuple[List, List, List]:
        failed_upload_list: list = []
        success_upload_list: list = []
        error: list = []
        for attachment in files:
            FILE_SOURCE: str = os.getenv('OCR_IMAGE_SOURCE_FOLDER')
            bucket_id: str = os.getcwd() + FILE_SOURCE
            Path(bucket_id).mkdir(parents=True, exist_ok=True)
            name, extension = attachment.filename.split(".")
            file_pattern: str = name + "(" + "%s" + ")" + "." + extension
            main_file_name: str = name + "." + extension
            file_name: str = next_file_name(file_pattern, bucket_id, main_file_name)
            print(attachment.filename)
            if extension in image_file_extensions:
                try:
                    with open(bucket_id + file_name, 'wb') as f:
                        f.write(attachment.file.read())
                    success_upload_list.append(attachment.filename)
                    item = OcrDataCreate(file_path=bucket_id + file_name)
                    OcrToolCrud(db=db).store(item=jsonable_encoder(item))
                    try:
                        db.commit()
                    except SQLAlchemyError as e:
                        db.rollback()
                        error.append(str(e.__dict__))

                except Exception as e:
                    print("Failed: ", e)
                    failed_upload_list.append(attachment.filename)
                    error.append(str(e.__dict__))

        return failed_upload_list, success_upload_list, error

    @staticmethod
    def get_ocr_data_by_id(db, id_: int):
        return OcrToolCrud(db=db).get(id_=id_)

    @staticmethod
    def get_ocr_data(db):
        return OcrToolCrud(db=db).gets()

    def get_character_images_and_class_to_be_classify(self, db, limit=5):
        final_image_object_list = []
        class_label_object = ClassLabelCrud(db=db).get_by_round_robin()
        db.commit()

        label_image_paths = ImageClustering(db=db, class_id=class_label_object.class_id).apply_kmean()

        images_object_list: List[models.Characters] = CharacterCrud(db=db).get_images(limit=100)
        to_be_label_image_paths = [image_object.character_path for image_object in images_object_list]
        for index, img_path in enumerate(to_be_label_image_paths):
            to_be_label_image = io.imread(img_path, as_gray=True)
            label_image_1 = io.imread(label_image_paths[0], as_gray=True)
            label_image_2 = io.imread(label_image_paths[1], as_gray=True)
            label_image_3 = io.imread(label_image_paths[2], as_gray=True)
            avg_ssim = (ssim(label_image_1, to_be_label_image,
                             data_range=to_be_label_image.max() - to_be_label_image.min()) + \
                        ssim(label_image_2, to_be_label_image,
                             data_range=to_be_label_image.max() - to_be_label_image.min()) + \
                        ssim(label_image_3, to_be_label_image,
                             data_range=to_be_label_image.max() - to_be_label_image.min())) / 3

            final_image_object_list.append((images_object_list[index], avg_ssim))
        final_image_object_list = sorted(final_image_object_list, key=lambda x: x[1], reverse=True)
        final_image_object_list = [obj[0]  for obj in final_image_object_list[0: limit] ]
        return final_image_object_list, class_label_object

    @staticmethod
    def get_character_image_by_id(db, id_: int):
        return CharacterCrud(db=db).get(id_=id_)

    @staticmethod
    def update_character_image_class(db, id_: int, body: CharacterClassUpdate):
        image: models.Characters = CharacterCrud(db=db).get(id_=id_)
        item: CharacterUpdate = CharacterUpdate()
        if image.class_id != body.class_id and image.winner_label_count > 0:
            item = CharacterUpdate(winner_label_count=image.winner_label_count - 1)
        elif image.winner_label_count == 0 or image.winner_label_count is None:
            item = CharacterUpdate(class_id=body.class_id,
                                   is_labeled=True,
                                   winner_label_count=1)
        elif 0 < image.winner_label_count < 3:
            item = CharacterUpdate(winner_label_count=image.winner_label_count + 1)
        response = CharacterCrud(db=db).update(item=item, id_=id_)
        db.commit()
        return response

    @staticmethod
    def get_images_for_class_label(db, class_id):
        image_paths = ImageClustering(db=db, class_id=class_id).apply_kmean()
        image_ids = [CharacterCrud(db=db).get_id_by_path(image_path) for image_path in image_paths]
        return image_ids
