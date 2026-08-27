# Harcama Takip API

Bu proje FastAPI öğrenmek icin gelistirdiğim basit bir harcama takip API projesidir.

1. haftada FastAPI temel endpoint işlemlerinı yaptım ve veriler Python listelerinde tuttum

2. haftada SQLite ve SQLAlchemy kullanılarak veritabanına gecirdim. Veriler artık veritabanında kalıcı olarak tutuluyor.

## Yapılan İşlemler

- Kategori ekleme
- Kategorileri listeleme
- Kategori güncelleme
- Kategori silme
- Harcama ekleme
- Harcamaları listeleme
- Harcama güncelleme
- Harcama silme
- Aynı isimde kategori eklenmesini engelleme
- Harcama tutarının 0'dan büyük olmasını kontrol etme
- Gelecek tarihli harcama eklenmesini engelleme
- Olmayan kategoriye harcama eklenmesini engelleme
- SQLite ile verileri kalıcı olarak saklama
- SQLAlchemy ile veritabanı işlemleri
- Depends ile veritabanı bağlantısı

## Kurulum

Gerekli paketleri yüklemek için:

```bash
pip install -r requirements.txt
```

## Çalıştırma

Projeyi çalıştırmak için:

```bash
uvicorn main:app --reload
```

Daha sonra tarayıcıdan aşağıdaki adrese gidilir:

```text
http://127.0.0.1:8000/docs
```

API işlemleri bu sayfa üzerinden test edilir.

## Kullanılan Teknolojiler

- Python
- FastAPI
- Pydantic
- Uvicorn
- SQLite
- SQLAlchemy