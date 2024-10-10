from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import database
from services import caching
from services.transformer import transformer_function, interleave_lists, generate_hash

router = APIRouter()

@router.post("/payload")
async def create_payload(payload: dict, db: Session = Depends(database.get_db)):
    list_1 = payload.get("list_1")
    list_2 = payload.get("list_2")

    if len(list_1) != len(list_2):
        raise HTTPException(status_code=400, detail="Both lists must have the same length.")

    # Generate hash for the input to check if the payload already exists
    input_hash = generate_hash(list_1, list_2)

    # Check if the outcome is already cached
    cached = caching.get_cached_outcome_by_hash(db, input_hash)
    if cached:
        return {"id": cached.id}

    # Simulate external service by transforming strings
    transformed_list_1 = [transformer_function(s) for s in list_1]
    transformed_list_2 = [transformer_function(s) for s in list_2]

    # Interleave the two lists
    result = interleave_lists(transformed_list_1, transformed_list_2)
    payload_output = ", ".join(result)

    # Store in database
    new_cached_outcome = caching.create_cached_outcome(db, input_hash, payload_output)

    return {"id": new_cached_outcome.id}

@router.get("/payload/{id}")
async def get_payload(id: int, db: Session = Depends(database.get_db)):
    cached = caching.get_cached_outcome_by_id(db, id)
    if not cached:
        raise HTTPException(status_code=404, detail="Payload not found")
    return {"output": cached.payload}