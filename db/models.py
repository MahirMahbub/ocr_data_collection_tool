import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import ARRAY

from db.database import Base


class ModelBase:
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    update_time = Column(DateTime(timezone=True), onupdate=datetime.datetime.utcnow, default=None)


class Characters(Base,ModelBase):
    __tablename__: str = "characters"

    character_path = Column(String, nullable=False)
    class_id = Column(String, nullable=True)
    inner_class_cluster_id = Column(String, nullable=True)
    is_labeled = Column(Boolean, default=False)
    winner_label_count = Column(Integer, default=0)


class NearestClassOfCharacter(Base,ModelBase):
    __tablename__: str = "nearest_class_of_character"
    character_id = Column(Integer, nullable=False)
    class_id = Column(String, nullable=False)
    inner_class_cluster_id = Column(String, nullable=False)
    similarity = Column(Float, nullable=False)
    is_valid_class = Column(Boolean)


class ClassLabel(Base,ModelBase):
    __tablename__: str = "class_label"
    class_id = Column(Integer, nullable=False)
    round_robin_marker = Column(Integer, default=0)


class OcrData(Base,ModelBase):
    __tablename__: str = "ocr_data"
    file_path = Column(String)
    is_extracted = Column(Boolean, default=False)


class Properties(Base,ModelBase):
    __tablename__: str = "properties"
    name = Column(String)
    value = Column(Boolean, default=False)


class ResponseReport(Base,ModelBase):
    __tablename__: str = "response_report"
    class_id = Column(Integer, default=None)
    num_character_label = Column(Integer, default=None)


class LabelCluster(Base,ModelBase):
    __tablename__: str = "label_cluster"
    character_paths = Column(ARRAY(String()))
    class_id = Column(Integer, default=None)
    number_of_image = Column(Integer, default=None)


class ScheduleJobNames(str, Enum):
    CharacterExtractorManager = "CharacterExtractorManager"
    PrintJobManager = "PrintJobManager"
    PreOcrCharacterLoad = "PreOcrCharacterLoad"
    ClusterManager = "ClusterManager"
