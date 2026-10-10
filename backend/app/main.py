from fastapi import FastAPI

# Register related models before SQLAlchemy configures workspace relationships.
import app.db.models  # noqa: F401

from app.domains.workspace.routers.workspace_router import router as workspace_router

app = FastAPI(
    title="KnowledgeOS",
    version="0.1.0",
)

app.include_router(
    workspace_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "KnowledgeOS API",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }
