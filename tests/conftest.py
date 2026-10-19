import os
import tempfile
from importlib import import_module
from pathlib import Path

import pytest


_TEST_DIRECTORY = tempfile.TemporaryDirectory(prefix="student-intelligence-tests-")
os.environ["DB_PATH"] = str(Path(_TEST_DIRECTORY.name) / "students.db")


def pytest_sessionstart(session):
    from database.db_sqlite import init_db

    init_db()


@pytest.fixture(autouse=True)
def use_deterministic_model(monkeypatch):
    prediction_service = import_module("services.predict")

    class DeterministicModel:
        def predict(self, features):
            return [50.0]

    monkeypatch.setattr(
        prediction_service,
        "load_model",
        lambda: DeterministicModel(),
    )
