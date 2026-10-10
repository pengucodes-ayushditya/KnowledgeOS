"""Regression checks for the preexisting broken workspace service wiring."""
import asyncio
import json
import os
import unittest
from unittest.mock import Mock, patch

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, configure_mappers
from sqlalchemy.pool import StaticPool

import app.db.models
from app.domains.workspace.models.workspace import Workspace
from app.domains.workspace.schemas.workspace import WorkspaceCreate
from app.domains.workspace.services.workspace_service import WorkspaceService


class WorkspaceTests(unittest.TestCase):
    def test_workspace_http_create_and_list(self):
        with patch.dict(os.environ, {"DATABASE_URL": "sqlite:///:memory:",
                                    "SECRET_KEY": "synthetic-test-setting"}):
            from app.main import app
            from app.db.session import get_db
        engine = create_engine("sqlite://", connect_args={"check_same_thread": False},
                               poolclass=StaticPool)
        Workspace.__table__.create(engine)

        def database():
            with Session(engine, expire_on_commit=False) as session:
                yield session

        async def request(method, body=b""):
            messages = []
            async def receive():
                return {"type": "http.request", "body": body, "more_body": False}
            async def send(message):
                messages.append(message)
            scope = {"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
                     "method": method, "scheme": "http", "path": "/api/v1/workspaces",
                     "raw_path": b"/api/v1/workspaces", "query_string": b"",
                     "root_path": "", "headers": [(b"content-type", b"application/json")],
                     "server": ("test", 80), "client": ("test", 123)}
            await app(scope, receive, send)
            status = next(m["status"] for m in messages if m["type"] == "http.response.start")
            content = b"".join(m.get("body", b"") for m in messages if m["type"] == "http.response.body")
            return status, json.loads(content)

        app.dependency_overrides[get_db] = database
        try:
            status, created = asyncio.run(request("POST", b'{"name":"HTTP fixture"}'))
            self.assertEqual(status, 200)
            status, listed = asyncio.run(request("GET"))
            self.assertEqual(status, 200)
            self.assertEqual(listed[0]["id"], created["id"])
        finally:
            app.dependency_overrides.clear()
            engine.dispose()

    def test_all_model_relationships_configure(self):
        configure_mappers()

    def test_workspace_creation_persists_between_sessions(self):
        engine = create_engine("sqlite:///:memory:")
        Workspace.__table__.create(engine)
        with Session(engine, expire_on_commit=False) as session:
            workspace = WorkspaceService(session).create_workspace(
                WorkspaceCreate(name="Example", description="Regression fixture"))
            self.assertIsNotNone(workspace.id)
        with Session(engine) as session:
            workspaces = WorkspaceService(session).list_workspaces()
            self.assertEqual([w.name for w in workspaces], ["Example"])
        engine.dispose()

    def test_failed_create_rolls_back(self):
        session = Mock()
        service = WorkspaceService(session)
        service.repository = Mock()
        service.repository.create.side_effect = RuntimeError("fixture failure")
        with self.assertRaises(RuntimeError):
            service.create_workspace(WorkspaceCreate(name="Example"))
        session.rollback.assert_called_once()
        session.commit.assert_not_called()
