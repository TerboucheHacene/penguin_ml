from pydantic import BaseModel, BaseSettings
from enum import Enum
from pathlib import Path


class Island(str, Enum):
    DREAM = "Dream"
    TORGERSEN = "Torgersen"
    BISCOE = "Biscoe"


class Sex(str, Enum):
    MALE = "Male"
    FEMALE = "Female"


class Species(str, Enum):
    CHINSTRAP = "Chinstrap"
    ADELIE = "Adelie"
    GENTOO = "Gentoo"


class PenguinBase(BaseModel):
    bill_length_mm: float
    bill_depth_mm: float
    flipper_length_mm: float
    body_mass_g: int


class PenguinDataInput(PenguinBase):
    island: Island
    sex: Sex


class PenguinModelInput(PenguinBase):
    island_biscoe: int
    island_dream: int
    island_torgerson: int
    sex_female: int
    sex_male: int


class PenguinClassOutput(BaseModel):
    species: Species


class Settings(BaseModel):
    model_path: Path
    unique_mapping: Path
