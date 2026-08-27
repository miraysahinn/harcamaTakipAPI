from fastapi import FastAPI, HTTPException, Depends, Response
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session
from datetime import date

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Harcama Takip API",
    description="FastAPI Harcama Takip Projesi",
    version="2.0"
)


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


@app.get("/")
def ana_sayfa():
    return {"mesaj": "Harcama Takip API çalışıyor"}


@app.post("/kategoriler", response_model=KategoriResponse, status_code=201)
def kategori_ekle(
    kategori: KategoriCreate,
    db: Session = Depends(get_db)
):
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


@app.get("/kategoriler", response_model=list[KategoriResponse])
def kategorileri_getir(
    db: Session = Depends(get_db)
):
    return db.query(models.Kategori).all()


@app.get("/kategoriler/{kategori_id}", response_model=KategoriResponse)
def kategori_getir(
    kategori_id: int,
    db: Session = Depends(get_db)
):
    kategori = db.query(models.Kategori).filter(
        models.Kategori.id == kategori_id
    ).first()

    if not kategori:
        raise HTTPException(
            status_code=404,
            detail="Kategori bulunamadı"
        )

    return kategori


@app.put("/kategoriler/{kategori_id}", response_model=KategoriResponse)
def kategori_guncelle(
    kategori_id: int,
    yeni_kategori: KategoriCreate,
    db: Session = Depends(get_db)
):
    kategori = db.query(models.Kategori).filter(
        models.Kategori.id == kategori_id
    ).first()

    if not kategori:
        raise HTTPException(
            status_code=404,
            detail="Kategori bulunamadı"
        )

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


@app.delete("/kategoriler/{kategori_id}", status_code=204)
def kategori_sil(
    kategori_id: int,
    db: Session = Depends(get_db)
):
    kategori = db.query(models.Kategori).filter(
        models.Kategori.id == kategori_id
    ).first()

    if not kategori:
        raise HTTPException(
            status_code=404,
            detail="Kategori bulunamadı"
        )

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

    return Response(status_code=204)


@app.post("/harcamalar", response_model=HarcamaResponse, status_code=201)
def harcama_ekle(
    harcama: HarcamaCreate,
    db: Session = Depends(get_db)
):
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


@app.get("/harcamalar", response_model=list[HarcamaResponse])
def harcamalari_getir(
    kategori_id: int | None = None,
    db: Session = Depends(get_db)
):
    sorgu = db.query(models.Harcama)

    if kategori_id is not None:
        sorgu = sorgu.filter(
            models.Harcama.kategori_id == kategori_id
        )

    return sorgu.all()


@app.get("/harcamalar/{harcama_id}", response_model=HarcamaResponse)
def harcama_getir(
    harcama_id: int,
    db: Session = Depends(get_db)
):
    harcama = db.query(models.Harcama).filter(
        models.Harcama.id == harcama_id
    ).first()

    if not harcama:
        raise HTTPException(
            status_code=404,
            detail="Harcama bulunamadı"
        )

    return harcama


@app.put("/harcamalar/{harcama_id}", response_model=HarcamaResponse)
def harcama_guncelle(
    harcama_id: int,
    yeni_harcama: HarcamaCreate,
    db: Session = Depends(get_db)
):
    harcama = db.query(models.Harcama).filter(
        models.Harcama.id == harcama_id
    ).first()

    if not harcama:
        raise HTTPException(
            status_code=404,
            detail="Harcama bulunamadı"
        )

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


@app.delete("/harcamalar/{harcama_id}", status_code=204)
def harcama_sil(
    harcama_id: int,
    db: Session = Depends(get_db)
):
    harcama = db.query(models.Harcama).filter(
        models.Harcama.id == harcama_id
    ).first()

    if not harcama:
        raise HTTPException(
            status_code=404,
            detail="Harcama bulunamadı"
        )

    db.delete(harcama)
    db.commit()

    return Response(status_code=204)