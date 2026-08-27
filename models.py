from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from database import Base


class Kategori(Base):
    __tablename__ = "kategoriler"

    id = Column(Integer, primary_key=True, index=True)
    isim = Column(String, unique=True, nullable=False)


class Harcama(Base):
    __tablename__ = "harcamalar"

    id = Column(Integer, primary_key=True, index=True)
    tutar = Column(Float, nullable=False)
    aciklama = Column(String, nullable=False)
    tarih = Column(Date, nullable=False)
    kategori_id = Column(
        Integer,
        ForeignKey("kategoriler.id"),
        nullable=False
    )