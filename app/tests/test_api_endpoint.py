import os
import pytest
from fastapi.testclient import TestClient
from main import app
from db import database, models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Path for the SQLite database file
TEST_DATABASE_URL = "sqlite:///./test_database.db"

# Create the SQLite engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    # Override the default database session with the testing one
    models.Base.metadata.create_all(bind=engine)
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[database.get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    # Remove the database file after tests are complete
    os.remove("test_database.db")

def test_create_payload(client):
    payload = {
        "list_1": ["first string", "second string", "third string"],
        "list_2": ["other string", "another string", "last string"]
    }
    response = client.post("/payload", json=payload)
    assert response.status_code == 200
    assert "id" in response.json()

def test_get_payload(client):
    # First, create a payload
    payload = {
        "list_1": ["first string", "second string", "third string"],
        "list_2": ["other string", "another string", "last string"]
    }
    response = client.post("/payload", json=payload)
    assert response.status_code == 200
    payload_id = response.json()["id"]

    # Now fetch the payload by ID
    response = client.get(f"/payload/{payload_id}")
    assert response.status_code == 200
    assert response.json()["output"] == "FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING, THIRD STRING, LAST STRING"
