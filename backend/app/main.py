from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import get_db

app = FastAPI(title="Order Tracking API")


@app.post("/track", response_model=list[schemas.TrackingResponse])
def track_items(request: schemas.TrackingBatchRequest, db: Session = Depends(get_db)):
    results = crud.get_tracking_batch(db, request.item_numbers)
    return results


@app.get("/track/{item_number}", response_model=schemas.TrackingResponse)
def track_single_item(item_number: str, db: Session = Depends(get_db)):
    result = crud.get_tracking_by_item_number(db, item_number)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result


@app.get("/track/batch/", response_model=list[schemas.TrackingResponse])
def track_batch(
    item_numbers: list[str] = Query(..., max_length=10),
    db: Session = Depends(get_db),
):
    results = crud.get_tracking_batch(db, item_numbers)
    return results
