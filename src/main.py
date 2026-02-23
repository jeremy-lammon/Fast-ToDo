from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.users.routes import UserRouter
from src.tasks.routes import TaskRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"Starting Todo App")
    from src.database.base_class import init_db
    await init_db()

    yield
    print(f"Shutting down Todo App")

app = FastAPI(title="Todo App", description="A Todo App backend built in FastAPI with modern practices", version="2.0.0", lifespan=lifespan)

# Add CORS middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Todo App"}

app.include_router(UserRouter)
app.include_router(TaskRouter)

