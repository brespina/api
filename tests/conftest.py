import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base
from app.deps import get_db
from app.main import app

# ---------------------------------------------------------------------
# 1. Spin up a *temporary* SQLite DB for every test session.
#    (Isolated, fast, no risk to prod data.)
# ---------------------------------------------------------------------
SQLALCHEMY_TEST_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=engine)   # create tables once per session
    yield
    Base.metadata.drop_all(bind=engine)     # clean up

# ---------------------------------------------------------------------
# 2. DB session fixture — new transaction per *function*
# ---------------------------------------------------------------------
@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

# ---------------------------------------------------------------------
# 3. Override FastAPI’s get_db dependency to plug in our test session
# ---------------------------------------------------------------------
@pytest.fixture
def client(db_session):
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
