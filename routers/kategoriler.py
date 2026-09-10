from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

import schemas
from database import get_db
from services import kategori_service


router = APIRouter(
    prefix="/kategoriler",
    tags=["Kategoriler"]
)


@router.post("", response_model=schemas.KategoriResponse, status_code=201)
def kategori_ekle(
    kategori: schemas.KategoriCreate,
    db: Session = Depends(get_db)
):
    return kategori_service.kategori_ekle(db, kategori)


@router.get("", response_model=list[schemas.KategoriResponse])
def kategorileri_getir(
    db: Session = Depends(get_db)
):
    return kategori_service.kategorileri_getir(db)


@router.get("/{kategori_id}", response_model=schemas.KategoriResponse)
def kategori_getir(
    kategori_id: int,
    db: Session = Depends(get_db)
):
    return kategori_service.kategori_getir(db, kategori_id)


@router.put("/{kategori_id}", response_model=schemas.KategoriResponse)
def kategori_guncelle(
    kategori_id: int,
    yeni_kategori: schemas.KategoriCreate,
    db: Session = Depends(get_db)
):
    return kategori_service.kategori_guncelle(
        db,
        kategori_id,
        yeni_kategori
    )


@router.delete("/{kategori_id}", status_code=204)
def kategori_sil(
    kategori_id: int,
    db: Session = Depends(get_db)
):
    kategori_service.kategori_sil(db, kategori_id)

    return Response(status_code=204)