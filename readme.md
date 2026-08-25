# Harcama Takip API

Bu proje FastAPI öğrenmek icin gelistirdiğim basit bir harcama takip API projesidir.

İlk hafta veriler veritabanı kullanılmadan listelerde tutulmaktadır.

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

## Kurulum

Gerekli paketleri yüklemek icin:

```bash
pip install -r requirements.txt
```

## Çalıştırma

Projeyi calıştırmak için:

```bash
uvicorn main:app --reload
```

sonra tarayıcıdan aşağıdaki adrese gidilir:

```text
http://127.0.0.1:8000/docs
```

API işlemleri bu sayfa üzerinden test edilir.

## Kullanılan Teknolojiler

- Python
- FastAPI
- Pydantic
- Uvicorn