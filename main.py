from fastapi import FastAPI

import models
from database import engine
from routers import kategoriler, harcamalar, rapor


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Harcama Takip API",
    description="FastAPI Harcama Takip Projesi",
    version="4.0"
)


app.include_router(kategoriler.router)
app.include_router(harcamalar.router)
app.include_router(rapor.router)


@app.get("/")
def ana_sayfa():
    return {"mesaj": "Harcama Takip API çalışıyor"}