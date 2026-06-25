from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def isolated_activities():
    """Ensure each test runs with a clean copy of the in-memory activity store."""
    snapshot = deepcopy(activities)
    try:
        yield activities
    finally:
        activities.clear()
        activities.update(snapshot)
