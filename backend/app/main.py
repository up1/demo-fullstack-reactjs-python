from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from . import crud, schemas
from .database import get_db, engine
from .cache import get_cached, set_cached
from .tracing import setup_tracing

app = FastAPI(title="Order Tracking API")
setup_tracing(app, engine)


def _serialize(item):
    return schemas.TrackingResponse.model_validate(item).model_dump(mode="json")


@app.post("/track", response_model=list[schemas.TrackingResponse])
def track_items(request: schemas.TrackingBatchRequest, db: Session = Depends(get_db)):
    results = []
    missing = []
    for num in request.item_numbers:
        cached = get_cached(f"track:{num}")
        if cached:
            results.append(cached)
        else:
            missing.append(num)
    if missing:
        db_results = crud.get_tracking_batch(db, missing)
        for item in db_results:
            data = _serialize(item)
            set_cached(f"track:{item.item_number}", data)
            results.append(data)
    return results


@app.get("/track/{item_number}", response_model=schemas.TrackingResponse)
def track_single_item(item_number: str, db: Session = Depends(get_db)):
    cached = get_cached(f"track:{item_number}")
    if cached:
        return cached
    result = crud.get_tracking_by_item_number(db, item_number)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    set_cached(f"track:{item_number}", _serialize(result))
    return result


@app.get("/track/batch/", response_model=list[schemas.TrackingResponse])
def track_batch(
    item_numbers: list[str] = Query(..., max_length=10),
    db: Session = Depends(get_db),
):
    results = []
    missing = []
    for num in item_numbers:
        cached = get_cached(f"track:{num}")
        if cached:
            results.append(cached)
        else:
            missing.append(num)
    if missing:
        db_results = crud.get_tracking_batch(db, missing)
        for item in db_results:
            data = _serialize(item)
            set_cached(f"track:{item.item_number}", data)
            results.append(data)
    return results
