from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date

import models
import schemas


def harcama_ekle(db: Session, harcama: schemas.HarcamaCreate):
    kategori = db.query(models.Kategori).filter(
        models.Kategori.id == harcama.kategori_id
    ).first()

    if not kategori:
        raise HTTPException(
            status_code=404,
            detail="Kategori bulunamadı"
        )

    if harcama.tarih > date.today():
        raise HTTPException(
            status_code=422,
            detail="Harcama tarihi gelecekte olamaz"
        )

    yeni_harcama = models.Harcama(
        tutar=harcama.tutar,
        aciklama=harcama.aciklama,
        tarih=harcama.tarih,
        kategori_id=harcama.kategori_id
    )

    db.add(yeni_harcama)
    db.commit()
    db.refresh(yeni_harcama)

    return yeni_harcama


def harcamalari_getir(
    db: Session,
    kategori_id: int | None = None,
    baslangic_tarihi: date | None = None,
    bitis_tarihi: date | None = None,
    min_tutar: float | None = None,
    max_tutar: float | None = None,
    limit: int = 10,
    offset: int = 0
):
    if limit <= 0:
        raise HTTPException(
            status_code=422,
            detail="Limit 0'dan büyük olmalıdır"
        )

    if offset < 0:
        raise HTTPException(
            status_code=422,
            detail="Offset negatif olamaz"
        )

    if min_tutar is not None and min_tutar < 0:
        raise HTTPException(
            status_code=422,
            detail="Minimum tutar negatif olamaz"
        )

    if max_tutar is not None and max_tutar < 0:
        raise HTTPException(
            status_code=422,
            detail="Maksimum tutar negatif olamaz"
        )

    if (
        min_tutar is not None
        and max_tutar is not None
        and min_tutar > max_tutar
    ):
        raise HTTPException(
            status_code=422,
            detail="Minimum tutar maksimum tutardan büyük olamaz"
        )

    if (
        baslangic_tarihi is not None
        and bitis_tarihi is not None
        and baslangic_tarihi > bitis_tarihi
    ):
        raise HTTPException(
            status_code=422,
            detail="Başlangıç tarihi bitiş tarihinden büyük olamaz"
        )

    sorgu = db.query(models.Harcama)

    if kategori_id is not None:
        sorgu = sorgu.filter(
            models.Harcama.kategori_id == kategori_id
        )

    if baslangic_tarihi is not None:
        sorgu = sorgu.filter(
            models.Harcama.tarih >= baslangic_tarihi
        )

    if bitis_tarihi is not None:
        sorgu = sorgu.filter(
            models.Harcama.tarih <= bitis_tarihi
        )

    if min_tutar is not None:
        sorgu = sorgu.filter(
            models.Harcama.tutar >= min_tutar
        )

    if max_tutar is not None:
        sorgu = sorgu.filter(
            models.Harcama.tutar <= max_tutar
        )

    return sorgu.offset(offset).limit(limit).all()


def harcama_getir(db: Session, harcama_id: int):
    harcama = db.query(models.Harcama).filter(
        models.Harcama.id == harcama_id
    ).first()

    if not harcama:
        raise HTTPException(
            status_code=404,
            detail="Harcama bulunamadı"
        )

    return harcama


def harcama_guncelle(
    db: Session,
    harcama_id: int,
    yeni_harcama: schemas.HarcamaCreate
):
    harcama = harcama_getir(db, harcama_id)

    kategori = db.query(models.Kategori).filter(
        models.Kategori.id == yeni_harcama.kategori_id
    ).first()

    if not kategori:
        raise HTTPException(
            status_code=404,
            detail="Kategori bulunamadı"
        )

    if yeni_harcama.tarih > date.today():
        raise HTTPException(
            status_code=422,
            detail="Harcama tarihi gelecekte olamaz"
        )

    harcama.tutar = yeni_harcama.tutar
    harcama.aciklama = yeni_harcama.aciklama
    harcama.tarih = yeni_harcama.tarih
    harcama.kategori_id = yeni_harcama.kategori_id

    db.commit()
    db.refresh(harcama)

    return harcama


def harcama_sil(db: Session, harcama_id: int):
    harcama = harcama_getir(db, harcama_id)

    db.delete(harcama)
    db.commit()