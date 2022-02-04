from enum import Enum

from sqlalchemy import Boolean, Column, Integer, String, Float

from db.database import Base


class Characters(Base):
    __tablename__: str = "characters"
    id = Column(Integer, primary_key=True, autoincrement=True)
    character_path = Column(String, nullable=False)
    class_id = Column(String, nullable=True)
    inner_class_cluster_id = Column(String, nullable=True)
    is_labeled = Column(Boolean, default=False)
    winner_label_count = Column(Integer, default=0)


class NearestClassOfCharacter(Base):
    __tablename__: str = "nearest_class_of_character"
    id = Column(Integer, primary_key=True, autoincrement=True)
    character_id = Column(Integer, nullable=False)
    class_id = Column(String, nullable=False)
    inner_class_cluster_id = Column(String, nullable=False)
    similarity = Column(Float, nullable=False)
    is_valid_class = Column(Boolean)


class ClassLabel(Base):
    __tablename__: str = "class_label"
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(Integer, nullable=False)
    round_robin_marker = Column(Integer, default=0)


class OcrData(Base):
    __tablename__: str = "ocr_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String)
    is_extracted = Column(Boolean, default=False)


class Properties(Base):
    __tablename__: str = "properties"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    value = Column(Boolean, default=False)


class ScheduleJobNames(str, Enum):
    CharacterExtractorManager = "CharacterExtractorManager"
    PrintJobManager = "PrintJobManager"
    PreOcrCharacterLoad = "PreOcrCharacterLoad"
