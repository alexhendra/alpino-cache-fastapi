import os
import pytest
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import models
from services import caching

log = logging.getLogger(__name__)

# Path for the SQLite database file
TEST_DATABASE_URL = "sqlite:///./test_database.db"

# Create the SQLite engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Set up the database tables
@pytest.fixture(scope="module")
def db():
    # Create the database tables
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    # Remove the database file after tests are complete
    os.remove("test_database.db")

def test_create_and_get_cached_outcome(db):
    input_hash = "testhash"
    payload = "TEST PAYLOAD"

    # Test create_cached_outcome
    cached_outcome = caching.create_cached_outcome(db, input_hash, payload)
    log.info(f"input_hash:{input_hash} | cached_outcome.input_hash: {cached_outcome.input_hash}")
    assert cached_outcome.input_hash == input_hash
    assert cached_outcome.payload == payload

    # Test get_cached_outcome_by_id
    fetched_outcome = caching.get_cached_outcome_by_id(db, cached_outcome.id)
    assert fetched_outcome.input_hash == input_hash
    assert fetched_outcome.payload == payload

    # Test get_cached_outcome_by_hash
    fetched_outcome_by_hash = caching.get_cached_outcome_by_hash(db, input_hash)
    assert fetched_outcome_by_hash.input_hash == input_hash
    assert fetched_outcome_by_hash.payload == payload
