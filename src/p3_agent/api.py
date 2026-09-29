from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field

from p3_agent.agent import Phase3Agent


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_DIR = WORKSPACE_ROOT / "dashboard" / "agentic"
load_dotenv(WORKSPACE_ROOT / ".env", override=False)


class AskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    question: str = Field(min_length=1, max_length=1000)


def create_app(agent: Phase3Agent | None = None) -> FastAPI:
    app = FastAPI(title="Gold Data Agentic BI", version="0.1.0")
    app.state.agent = agent

    @app.get("/health", tags=["system"])
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "openai_configured": bool(os.getenv("OPENAI_API_KEY")) or agent is not None,
            "phase2_api_url": os.getenv("PHASE2_API_URL", "http://127.0.0.1:8100"),
        }

    @app.post("/api/ask", tags=["agent"])
    def ask(request: AskRequest) -> dict[str, Any]:
        current_agent = agent or Phase3Agent()
        try:
            result = current_agent.answer(request.question)
            return result
        except ValueError as error:
            raise HTTPException(status_code=422, detail=str(error)) from None
        except RuntimeError as error:
            status_code = 503 if "OPENAI_API_KEY" in str(error) else 502
            raise HTTPException(status_code=status_code, detail=str(error)) from None
        except Exception as error:
            # Do not return provider exception details, request data, or credentials to the browser.
            raise HTTPException(status_code=502, detail="The analytics request could not be completed. Check that Phase 2 and OpenAI are available.") from error
        finally:
            if agent is None:
                current_agent.close()

    @app.get("/", include_in_schema=False)
    def dashboard() -> FileResponse:
        return FileResponse(DASHBOARD_DIR / "index.html")

    app.mount("/static", StaticFiles(directory=DASHBOARD_DIR), name="phase3-static")
    return app


app = create_app()
