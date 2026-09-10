from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas


def kategori_ekle(db: Session, kategori: schemas.KategoriCreate):
    mevcut = db.query(models.Kategori).filter(
        models.Kategori.isim == kategori.isim
    ).first()

    if mevcut:
        raise HTTPException(
            status_code=422,
            detail="Bu kategori zaten var"
        )

    yeni_kategori = models.Kategori(
        isim=kategori.isim
    )

    db.add(yeni_kategori)
    db.commit()
    db.refresh(yeni_kategori)

    return yeni_kategori


def kategorileri_getir(db: Session):
    return db.query(models.Kategori).all()


def kategori_getir(db: Session, kategori_id: int):
    kategori = db.query(models.Kategori).filter(
        models.Kategori.id == kategori_id
    ).first()

    if not kategori:
        raise HTTPException(
            status_code=404,
            detail="Kategori bulunamadı"
        )

    return kategori


def kategori_guncelle(
    db: Session,
    kategori_id: int,
    yeni_kategori: schemas.KategoriCreate
):
    kategori = kategori_getir(db, kategori_id)

    ayni_isim = db.query(models.Kategori).filter(
        models.Kategori.isim == yeni_kategori.isim,
        models.Kategori.id != kategori_id
    ).first()

    if ayni_isim:
        raise HTTPException(
            status_code=422,
            detail="Bu kategori zaten var"
        )

    kategori.isim = yeni_kategori.isim

    db.commit()
    db.refresh(kategori)

    return kategori


def kategori_sil(db: Session, kategori_id: int):
    kategori = kategori_getir(db, kategori_id)

    harcama_var = db.query(models.Harcama).filter(
        models.Harcama.kategori_id == kategori_id
    ).first()

    if harcama_var:
        raise HTTPException(
            status_code=422,
            detail="Bu kategoriye ait harcamalar var"
        )

    db.delete(kategori)
    db.commit()