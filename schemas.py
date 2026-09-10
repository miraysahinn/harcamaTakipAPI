from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class KategoriCreate(BaseModel):
    isim: str


class KategoriResponse(BaseModel):
    id: int
    isim: str

    model_config = ConfigDict(from_attributes=True)


class HarcamaCreate(BaseModel):
    tutar: float = Field(gt=0)
    aciklama: str
    tarih: date
    kategori_id: int


class HarcamaResponse(BaseModel):
    id: int
    tutar: float
    aciklama: str
    tarih: date
    kategori_id: int

    model_config = ConfigDict(from_attributes=True)