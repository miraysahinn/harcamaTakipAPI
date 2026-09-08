# Harcama Takip API

Bu proje FastAPI öğrenmek amacıyla geliştirdiğim basit bir harcama takip API projesidir.

1. haftada FastAPI temel endpoint işlemleri yapıldı ve veriler Python listelerinde tutuldu.

2. haftada SQLite ve SQLAlchemy kullanılarak veritabanına geçildi. Veriler artık veritabanında kalıcı olarak tutulmaktadır.

3. haftada harcamalar için kategori, tarih aralığı, minimum ve maksimum tutar filtreleri eklendi. Limit ve offset ile sayfalama yapıldı. Ayrıca aylık harcama raporu oluşturuldu.

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
- Kategoriye göre harcama filtreleme
- Tarih aralığına göre harcama filtreleme
- Minimum ve maksimum tutara göre filtreleme
- Limit ve offset ile sayfalama
- Aylık harcama raporu
- Kategori bazlı ve genel toplam hesaplama

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

API işlemleri bu sayfa üzerinden test edilebilir.

## Kullanılan Teknolojiler

- Python
- FastAPI
- Pydantic
- Uvicorn
- SQLite
- SQLAlchemy