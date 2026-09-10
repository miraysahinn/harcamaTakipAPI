from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date

import models


def aylik_rapor(db: Session, yil: int, ay: int):
    if ay < 1 or ay > 12:
        raise HTTPException(
            status_code=422,
            detail="Ay 1 ile 12 arasında olmalıdır"
        )

    harcamalar = db.query(models.Harcama).filter(
        models.Harcama.tarih >= date(yil, ay, 1)
    ).all()

    aylik_harcamalar = []

    for harcama in harcamalar:
        if harcama.tarih.year == yil and harcama.tarih.month == ay:
            aylik_harcamalar.append(harcama)

    kategori_toplamlari = {}
    genel_toplam = 0

    for harcama in aylik_harcamalar:
        kategori = db.query(models.Kategori).filter(
            models.Kategori.id == harcama.kategori_id
        ).first()

        kategori_ismi = kategori.isim

        if kategori_ismi not in kategori_toplamlari:
            kategori_toplamlari[kategori_ismi] = 0

        kategori_toplamlari[kategori_ismi] += harcama.tutar
        genel_toplam += harcama.tutar

    return {
        "yil": yil,
        "ay": ay,
        "kategori_toplamlari": kategori_toplamlari,
        "genel_toplam": genel_toplam
    }