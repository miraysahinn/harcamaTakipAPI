from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_ana_sayfa():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "mesaj": "Harcama Takip API çalışıyor"
    }


def test_kategorileri_getir():
    response = client.get("/kategoriler")

    assert response.status_code == 200


def test_olmayan_kategori():
    response = client.get("/kategoriler/99999")

    assert response.status_code == 404

def test_hatali_limit():
    response = client.get("/harcamalar?limit=0")

    assert response.status_code == 422

def test_hatali_tutar_araligi():
    response = client.get(
        "/harcamalar?min_tutar=500&max_tutar=100"
    )

    assert response.status_code == 422