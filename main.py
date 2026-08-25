from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
from datetime import date

app = FastAPI(
    title="Harcama Takip API",
    description="1. Hafta - FastAPI temel CRUD işlemleri",
    version="1.0"
)

kategoriler = []
harcamalar = []


class KategoriCreate(BaseModel):
    isim: str


class KategoriResponse(BaseModel):
    id: int
    isim: str


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


@app.get("/")
def ana_sayfa():
    return {"mesaj": "Harcama Takip API çalışıyor"}


@app.post("/kategoriler", response_model=KategoriResponse, status_code=201)
def kategori_ekle(kategori: KategoriCreate):
    for k in kategoriler:
        if k["isim"].lower() == kategori.isim.lower():
            raise HTTPException(
                status_code=422,
                detail="Bu kategori zaten var"
            )

    yeni_id = max([k["id"] for k in kategoriler], default=0) + 1

    yeni_kategori = {
        "id": yeni_id,
        "isim": kategori.isim
    }

    kategoriler.append(yeni_kategori)
    return yeni_kategori


@app.get("/kategoriler", response_model=list[KategoriResponse])
def kategorileri_getir():
    return kategoriler


@app.get("/kategoriler/{kategori_id}", response_model=KategoriResponse)
def kategori_getir(kategori_id: int):
    for kategori in kategoriler:
        if kategori["id"] == kategori_id:
            return kategori

    raise HTTPException(
        status_code=404,
        detail="Kategori bulunamadı"
    )


@app.put("/kategoriler/{kategori_id}", response_model=KategoriResponse)
def kategori_guncelle(kategori_id: int, yeni_kategori: KategoriCreate):
    for kategori in kategoriler:
        if kategori["id"] == kategori_id:
            for k in kategoriler:
                if (
                    k["isim"].lower() == yeni_kategori.isim.lower()
                    and k["id"] != kategori_id
                ):
                    raise HTTPException(
                        status_code=422,
                        detail="Bu kategori zaten var"
                    )

            kategori["isim"] = yeni_kategori.isim
            return kategori

    raise HTTPException(
        status_code=404,
        detail="Kategori bulunamadı"
    )


@app.delete("/kategoriler/{kategori_id}", status_code=204)
def kategori_sil(kategori_id: int):
    for kategori in kategoriler:
        if kategori["id"] == kategori_id:
            kategoriler.remove(kategori)
            return Response(status_code=204)

    raise HTTPException(
        status_code=404,
        detail="Kategori bulunamadı"
    )


@app.post("/harcamalar", response_model=HarcamaResponse, status_code=201)
def harcama_ekle(harcama: HarcamaCreate):
    kategori_var = False

    for kategori in kategoriler:
        if kategori["id"] == harcama.kategori_id:
            kategori_var = True
            break

    if not kategori_var:
        raise HTTPException(
            status_code=404,
            detail="Kategori bulunamadı"
        )

    if harcama.tarih > date.today():
        raise HTTPException(
            status_code=422,
            detail="Harcama tarihi gelecekte olamaz"
        )

    yeni_id = max([h["id"] for h in harcamalar], default=0) + 1

    yeni_harcama = {
        "id": yeni_id,
        "tutar": harcama.tutar,
        "aciklama": harcama.aciklama,
        "tarih": harcama.tarih,
        "kategori_id": harcama.kategori_id
    }

    harcamalar.append(yeni_harcama)
    return yeni_harcama


@app.get("/harcamalar", response_model=list[HarcamaResponse])
def harcamalari_getir(kategori_id: int | None = None):
    if kategori_id is None:
        return harcamalar

    sonuc = []

    for harcama in harcamalar:
        if harcama["kategori_id"] == kategori_id:
            sonuc.append(harcama)

    return sonuc


@app.get("/harcamalar/{harcama_id}", response_model=HarcamaResponse)
def harcama_getir(harcama_id: int):
    for harcama in harcamalar:
        if harcama["id"] == harcama_id:
            return harcama

    raise HTTPException(
        status_code=404,
        detail="Harcama bulunamadı"
    )


@app.put("/harcamalar/{harcama_id}", response_model=HarcamaResponse)
def harcama_guncelle(harcama_id: int, yeni_harcama: HarcamaCreate):
    kategori_var = False

    for kategori in kategoriler:
        if kategori["id"] == yeni_harcama.kategori_id:
            kategori_var = True
            break

    if not kategori_var:
        raise HTTPException(
            status_code=404,
            detail="Kategori bulunamadı"
        )

    if yeni_harcama.tarih > date.today():
        raise HTTPException(
            status_code=422,
            detail="Harcama tarihi gelecekte olamaz"
        )

    for harcama in harcamalar:
        if harcama["id"] == harcama_id:
            harcama["tutar"] = yeni_harcama.tutar
            harcama["aciklama"] = yeni_harcama.aciklama
            harcama["tarih"] = yeni_harcama.tarih
            harcama["kategori_id"] = yeni_harcama.kategori_id
            return harcama

    raise HTTPException(
        status_code=404,
        detail="Harcama bulunamadı"
    )


@app.delete("/harcamalar/{harcama_id}", status_code=204)
def harcama_sil(harcama_id: int):
    for harcama in harcamalar:
        if harcama["id"] == harcama_id:
            harcamalar.remove(harcama)
            return Response(status_code=204)

    raise HTTPException(
        status_code=404,
        detail="Harcama bulunamadı"
    )