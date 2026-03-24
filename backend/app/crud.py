from sqlalchemy.orm import Session
from . import models


def get_tracking_by_item_number(db: Session, item_number: str):
    return db.query(models.Tracking).filter(
        models.Tracking.item_number == item_number
    ).first()


def get_tracking_batch(db: Session, item_numbers: list[str]):
    return db.query(models.Tracking).filter(
        models.Tracking.item_number.in_(item_numbers)
    ).all()
