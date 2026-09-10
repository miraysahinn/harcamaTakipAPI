from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from datetime import date

import schemas
from database import get_db
from services import harcama_service


router = APIRouter(
    prefix="/harcamalar",
    tags=["Harcamalar"]
)


@router.post("", response_model=schemas.HarcamaResponse, status_code=201)
def harcama_ekle(
    harcama: schemas.HarcamaCreate,
    db: Session = Depends(get_db)
):
    return harcama_service.harcama_ekle(db, harcama)


@router.get("", response_model=list[schemas.HarcamaResponse])
def harcamalari_getir(
    kategori_id: int | None = None,
    baslangic_tarihi: date | None = None,
    bitis_tarihi: date | None = None,
    min_tutar: float | None = None,
    max_tutar: float | None = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    return harcama_service.harcamalari_getir(
        db,
        kategori_id,
        baslangic_tarihi,
        bitis_tarihi,
        min_tutar,
        max_tutar,
        limit,
        offset
    )


@router.get("/{harcama_id}", response_model=schemas.HarcamaResponse)
def harcama_getir(
    harcama_id: int,
    db: Session = Depends(get_db)
):
    return harcama_service.harcama_getir(db, harcama_id)


@router.put("/{harcama_id}", response_model=schemas.HarcamaResponse)
def harcama_guncelle(
    harcama_id: int,
    yeni_harcama: schemas.HarcamaCreate,
    db: Session = Depends(get_db)
):
    return harcama_service.harcama_guncelle(
        db,
        harcama_id,
        yeni_harcama
    )


@router.delete("/{harcama_id}", status_code=204)
def harcama_sil(
    harcama_id: int,
    db: Session = Depends(get_db)
):
    harcama_service.harcama_sil(db, harcama_id)

    return Response(status_code=204)