from sqlalchemy.orm import Session
from db import models

def get_cached_outcome_by_id(db: Session, id: int):
    """Retrieve a cached payload by its ID."""
    return db.query(models.CachedOutcome).filter(models.CachedOutcome.id == id).first()

def get_cached_outcome_by_hash(db: Session, input_hash: str):
    """Retrieve a cached payload by its hash."""
    return db.query(models.CachedOutcome).filter(models.CachedOutcome.input_hash == input_hash).first()

def create_cached_outcome(db: Session, input_hash: str, payload: str):
    """Create and store a new cached payload in the database."""
    new_cached_outcome = models.CachedOutcome(input_hash=input_hash, payload=payload)
    db.add(new_cached_outcome)
    db.commit()
    db.refresh(new_cached_outcome)
    return new_cached_outcome