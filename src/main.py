from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from src.db.connection import engine
from src.db.models import Base
from src.api.routes import agents, decisions, rounds, simulations
import uvicorn
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(
    title="AGENTIC-MAS-API", 
    version="1.0.0",
    lifespan=lifespan
)
@app.middleware("http")
async def method_override(request: Request, call_next):
    override = request.headers.get("X-HTTP-Method-Override")
    if override:
        request.scope["method"] = override.upper()
    return await call_next(request)

app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(decisions.router, prefix="/decisions", tags=["Decisions"])
app.include_router(rounds.router, prefix="/rounds", tags=["Rounds"])
app.include_router(simulations.router, prefix="/simulations", tags=["Simulations"])

@app.get("/", tags=["Health"])
def read_root():
    return {"message": "AGENTIC-MAS-API is running!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
