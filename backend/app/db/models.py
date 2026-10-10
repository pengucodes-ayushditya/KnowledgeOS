"""
Central registry for all SQLAlchemy ORM models.

Importing this module ensures every SQLAlchemy model is
registered with Base.metadata before Alembic autogeneration.
"""

# Workspace
from app.domains.workspace.models.workspace import Workspace

# Ingestion
from app.domains.ingestion.models.resource import Resource
from app.domains.ingestion.models.document import Document
from app.domains.ingestion.models.chunk import Chunk
from app.domains.ingestion.models.embedding import Embedding
from app.domains.ingestion.models.extraction_job import ExtractionJob

# Knowledge
from app.domains.knowledge.models.source import Source
from app.domains.knowledge.models.atom import KnowledgeAtom
from app.domains.knowledge.models.alias import Alias
from app.domains.knowledge.models.evidence import Evidence
from app.domains.knowledge.models.relationship import KnowledgeRelationship

__all__ = [
    "Workspace",
    "Resource",
    "Document",
    "Chunk",
    "Embedding",
    "ExtractionJob",
    "Source",
    "KnowledgeAtom",
    "Alias",
    "Evidence",
    "KnowledgeRelationship",
]