import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import api_router

# Create database tables on first run (swap for Alembic later)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coog Esports Admin API", version="0.1.0")

# Allow Vue dev-server hits from localhost:5173 by default
origins = [
    "http://localhost",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wire up every router
app.include_router(api_router)

# --------------------------------------------------------------------------
# Only needed when running directly:  `python -m app.main`
# (in prod you’ll run with `uvicorn app.main:app --host 0.0.0.0 --port 8000`)
# --------------------------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
