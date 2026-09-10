from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from services import rapor_service


router = APIRouter(
    prefix="/rapor",
    tags=["Rapor"]
)


@router.get("/aylik")
def aylik_rapor(
    yil: int,
    ay: int,
    db: Session = Depends(get_db)
):
    return rapor_service.aylik_rapor(
        db,
        yil,
        ay
    )