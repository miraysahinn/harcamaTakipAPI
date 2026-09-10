# Harcama Takip API

Bu proje FastAPI öğrenmek amacıyla geliştirdiğim bir harcama takip API projesidir.

Proje 4 hafta boyunca adım adım geliştirildi. İlk hafta temel API işlemleri yapıldı, sonraki haftalarda veritabanı, filtreleme, raporlama, katmanlı klasör yapısı ve test işlemleri eklendi.

## Proje Gelişim Süreci

### 1. Hafta

FastAPI temel endpoint işlemleri yapıldı.

- Path, query ve body parametreleri kullanıldı.
- Pydantic şemaları oluşturuldu.
- Kategori CRUD işlemleri yapıldı.
- Harcama CRUD işlemleri yapıldı.
- Veriler başlangıçta Python listelerinde tutuldu.
- Kategori isimlerinin benzersiz olması kontrol edildi.
- Harcama tutarının sıfırdan büyük olması kontrol edildi.
- Gelecek tarihli harcama eklenmesi engellendi.
- Olmayan kategoriye harcama eklenmesi engellendi.
- HTTP durum kodları kullanıldı.

### 2. Hafta

SQLite ve SQLAlchemy kullanılarak veritabanına geçildi.

- SQLite veritabanı oluşturuldu.
- SQLAlchemy modelleri oluşturuldu.
- Veriler kalıcı olarak veritabanında tutulmaya başlandı.
- Depends ile veritabanı bağlantısı kullanıldı.
- Olmayan kayıtlar için 404 hata yönetimi yapıldı.
- Kategori ve harcama işlemleri veritabanı ile çalışacak şekilde düzenlendi.

### 3. Hafta

Harcama filtreleme, sayfalama ve aylık rapor özellikleri eklendi.

- Kategoriye göre filtreleme yapıldı.
- Başlangıç ve bitiş tarihine göre filtreleme yapıldı.
- Minimum ve maksimum tutara göre filtreleme yapıldı.
- Limit ve offset ile sayfalama eklendi.
- Aylık harcama raporu oluşturuldu.
- Kategori bazlı toplam hesaplandı.
- Genel toplam hesaplandı.
- Kod router, service, model ve schema yapısına ayrıldı.

### 4. Hafta

Projenin testleri ve son kontrolleri yapıldı.

- FastAPI TestClient kullanıldı.
- pytest ile testler yazıldı.
- 5 farklı test oluşturuldu.
- Hatalı limit kontrolü test edildi.
- Hatalı tutar aralığı kontrolü test edildi.
- Olmayan kategori için 404 kontrolü test edildi.
- README dosyası güncellendi.
- Örnek API istekleri eklendi.

## Özellikler

- Kategori ekleme
- Kategorileri listeleme
- Kategori görüntüleme
- Kategori güncelleme
- Kategori silme
- Harcama ekleme
- Harcamaları listeleme
- Harcama görüntüleme
- Harcama güncelleme
- Harcama silme
- Harcamaları filtreleme
- Sayfalama
- Aylık rapor oluşturma
- Kategori bazlı toplam hesaplama
- Genel toplam hesaplama
- Veri doğrulama
- Hata yönetimi
- API testleri

## Proje Dosyaları

Projede kodları daha düzenli tutmak için dosyaları ayırdım.

- main.py
- database.py
- models.py
- schemas.py
- test_main.py
- requirements.txt
- .gitignore
- README.md

routers klasöründe:
- kategoriler.py
- harcamalar.py
- rapor.py

services klasöründe:
- kategori_service.py
- harcama_service.py
- rapor_service.py

Projede endpointler routers, veritabanı işlemleri ve kontroller ise services klasöründe bulunuyor. Veritabanı modelleri models.py, Pydantic şemaları schemas.py ve veritabanı bağlantısı database.py dosyasında bulunuyor.

## Kullanılan Teknolojiler

- Python
- FastAPI
- Pydantic
- Uvicorn
- SQLite
- SQLAlchemy
- pytest
- FastAPI TestClient
- httpx

## Kurulum

Projeyi bilgisayara indirdikten sonra proje klasöründe sanal ortam oluşturulur.

```bash
python -m venv venv
```

Windows Command Prompt üzerinden sanal ortam aktif edilir.

```bash
venv\Scripts\activate.bat
```

Gerekli paketler yüklenir.

```bash
pip install -r requirements.txt
```

## Projeyi Çalıştırma

API'yi çalıştırmak için:

```bash
uvicorn main:app --reload
```

Sunucu çalıştıktan sonra Swagger arayüzüne aşağıdaki adresten ulaşılabilir:

```text
http://127.0.0.1:8000/docs
```

API endpointleri bu sayfa üzerinden test edilebilir.

## Testler

Testler FastAPI TestClient ve pytest kullanılarak hazırlanmıştır.

Testleri calıştırmak için:

```bash
python -m pytest test_main.py -v
```

Projede 5 test bulunmaktadır.

Testler başarılı olduğunda terminalde:

```text
5 passed
```

sonucu görülür.

## Örnek İstekler

### Kategori Ekleme

POST `/kategoriler`

Örnek body:

```json
{
  "isim": "yemek"
}
```

### Kategorileri Listeleme

GET `/kategoriler`

### Kategori Görüntüleme

GET `/kategoriler/1`

### Harcama Ekleme

POST `/harcamalar`

Örnek body:

```json
{
  "tutar": 250,
  "aciklama": "Market alışverişi",
  "tarih": "2026-08-27",
  "kategori_id": 1
}
```

### Harcamaları Listeleme

GET `/harcamalar`

### Harcamaları Filtreleme

Örnek:

```text
/harcamalar?kategori_id=1&min_tutar=100&max_tutar=500&limit=10&offset=0
```

### Tarih Aralığına Göre Filtreleme

Örnek:

```text
/harcamalar?baslangic_tarihi=2026-08-01&bitis_tarihi=2026-08-31
```

### Sayfalama

Örnek:

```text
/harcamalar?limit=10&offset=0
```

### Aylık Rapor

GET:

```text
/rapor/aylik?yil=2026&ay=8
```

Örnek cevap:

```json
{
  "yil": 2026,
  "ay": 8,
  "kategori_toplamlari": {
    "yemek": 700
  },
  "genel_toplam": 700
}
```

## Validasyon ve Hata Yönetimi

Projede aşağıdaki kontroller bulunmaktadır.

- Harcama tutarı sıfırdan büyük olmalıdır.
- Harcama tarihi gelecekte olamaz.
- Olmayan bir kategoriye harcama eklenemez.
- Aynı isimde birden fazla kategori oluşturulamaz.
- Olmayan kayıtlar için 404 durum kodu döndürülür.
- Geçersiz veriler için 422 durum kodu döndürülür.
- Başarılı ekleme işlemlerinde 201 durum kodu kullanılır.
- Başarılı silme işlemlerinde 204 durum kodu kullanılır.
- Limit sıfırdan büyük olmalıdır.
- Offset negatif olamaz.
- Minimum tutar maksimum tutardan büyük olamaz.
- Başlangıç tarihi bitiş tarihinden büyük olamaz.