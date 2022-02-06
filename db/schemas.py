from typing import Optional

from fastapi_camelcase import CamelModel
from pydantic import BaseModel


class JobOptions(CamelModel):
    name: Optional[str] = None
    misfire_grace_time: Optional[int] = None
    coalesce: Optional[bool] = None
    max_runs: Optional[int] = None
    max_instances: Optional[int] = None


class OcrDataCreate(BaseModel):
    file_path: str


class OcrDataUpdate(BaseModel):
    id: Optional[int] = None
    is_extracted: Optional[bool] = None
    file_path: Optional[str] = None


class OcrDataGet(BaseModel):
    id: Optional[int] = None
    is_extracted: Optional[bool] = None
    file_path: Optional[str] = None

    # class Config:
    #     orm_mode = True


class CharacterCreate(BaseModel):
    character_path: str
    class_id: Optional[str] = None
    inner_class_cluster_id: Optional[str] = None
    is_labeled: Optional[bool] = None
    winner_label_count: Optional[int] = None


class ClassLabelCreate(BaseModel):
    class_id: str


class CharacterUpdate(BaseModel):
    character_path: Optional[str] = None
    class_id: Optional[str] = None
    inner_class_cluster_id: Optional[str] = None
    is_labeled: Optional[bool] = None
    winner_label_count: Optional[int] = None


class CharacterClassUpdate(BaseModel):
    class_id: Optional[str] = None
