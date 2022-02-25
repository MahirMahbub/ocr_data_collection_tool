import os
import time
from typing import List

import imageio
from fastapi.encoders import jsonable_encoder
from imageio import imsave
from sqlalchemy.exc import SQLAlchemyError

from app.cruds.character import CharacterCrud
from app.cruds.class_label import ClassLabelCrud
from app.cruds.label_cluster import LabelClusterCrud
from app.cruds.ocr_tools import OcrToolCrud
from app.custom_classes.image_clustering import ImageClustering
from app.custom_classes.ocr_character_seperator import OcrCharacterSeperator
from db import models
from db.database import SessionLocal
from db.schemas import CharacterCreate, OcrDataUpdate, ClassLabelCreate, LabelClusterCreate


class BaseJobManager(object):
    def __init__(self):
        self.db = SessionLocal()

    @staticmethod
    def execute():
        pass


class PrintJobManager(BaseJobManager):
    def __init__(self):
        super().__init__()

    def print_hello_activity(self, should_run):
        """Work Flow Start"""
        print("nabila")
        time.sleep(4)
        """Work Flow End"""

    @staticmethod
    def execute():
        PrintJobManager().print_hello_activity(should_run=True)


class PreOcrCharacterLoad(BaseJobManager):
    def __init__(self):
        super().__init__()

    def ocr_character_collection_activity(self, should_run):
        # preload_flag = self.db.query(models.Properties).filter(models.Properties.name == "CharacterDataPreLoad").first()
        # print(preload_flag)
        # if not preload_flag:
        current_path = os.getcwd()
        class_data_path = "/app/data/training_set/"
        list_dir = os.listdir(current_path + class_data_path)
        for class_name in list_dir:
            label_item = ClassLabelCreate(class_id=class_name)
            ClassLabelCrud(db=self.db).store(item=label_item, checker={"class_id": class_name})

            list_of_files = [current_path + class_data_path + os.path.join(class_name, f) for f in
                             os.listdir(current_path + class_data_path + class_name + "/")]
            for file in list_of_files:
                item = CharacterCreate(character_path=file,
                                       class_id=class_name,
                                       is_labeled=True)
                CharacterCrud(db=self.db).store(item=item, checker={"character_path": file})
            # self.db.commit()
        self.db.add(models.Properties(name="CharacterDataPreLoad", value=True))
        self.db.commit()

    @staticmethod
    def execute():
        PreOcrCharacterLoad().ocr_character_collection_activity(should_run=True)


class CharacterExtractorManager(BaseJobManager):
    def __init__(self):
        super().__init__()

    def character_extract_activity(self, should_run):
        ocr_processing_object: OcrCharacterSeperator = OcrCharacterSeperator()
        ocr_image_paths: List[models.OcrData] = OcrToolCrud(db=self.db).get_by_non_extracted()
        print(ocr_image_paths)
        # print(os.getcwd())
        for ocr_image in ocr_image_paths:
            images_and_save_path = ocr_processing_object.character_extractor(ocr_image.file_path)
            for save_path, char_img in images_and_save_path:
                # imageio.imwrite(save_path, char_img)
                imsave(save_path, char_img)
                item = CharacterCreate(character_path=save_path,
                                       winner_label_count=0,
                                       is_labeled=False)
                character_model_object = CharacterCrud(db=self.db).store(item)
                self.db.add(character_model_object)
            item = OcrDataUpdate(is_extracted=True)
            OcrToolCrud(db=self.db).update(id_=ocr_image.id, item=item)
            self.db.commit()

    @staticmethod
    def execute():
        CharacterExtractorManager().character_extract_activity(should_run=True)


class ClusterManager(BaseJobManager):
    def __init__(self):
        super().__init__()

    def cluster_activity(self, should_run):
        class_label_objects: List[models.ClassLabel] = ClassLabelCrud(db=self.db).gets()
        for class_label_object in class_label_objects:
            label_cluster_data: models.LabelCluster = LabelClusterCrud(db=self.db).get_by_class_id(
                class_id=class_label_object.class_id)
            number_of_image_labeled: models.Characters = CharacterCrud(db=self.db).get_count_by_class_id(
                class_id=str(class_label_object.class_id))
            # print(number_of_image_labeled, label_cluster_data)
            if label_cluster_data is None or label_cluster_data.number_of_image != number_of_image_labeled:
                label_image_paths = ImageClustering(db=self.db, class_id=class_label_object.class_id).apply_kmean()
                # print(label_image_paths)
                item = LabelClusterCreate(class_id=class_label_object.class_id,
                                          number_of_image=number_of_image_labeled,
                                          character_paths=label_image_paths)
                try:
                    crud_object = LabelClusterCrud(db=self.db).store(item=item)
                except SQLAlchemyError as e:
                    print(str(e.__dict__['orig']))
                    self.db.rollback()
            self.db.commit()

    @staticmethod
    def execute():
        ClusterManager().cluster_activity(should_run=True)
