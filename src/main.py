from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.users.routes import UserRouter
from src.tasks.routes import TaskRouter
from src.exceptions import AppError

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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "message": error["msg"],
                    "code": "VALIDATION_ERROR",
                    "field": (
                        ".".join(str(loc) for loc in error["loc"])
                        if error.get("loc")
                        else None
                    ),
                }
                for error in exc.errors()
            ]
        },
    )

@app.exception_handler(AppError)
async def custom_exception_handler(request: Request, exc: AppError):
    
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    
    return JSONResponse(
        status_code=500, 
        content={
            "detail": [
                {
                    "message": "An internal server error occured",
                    "code": "INTERNAL_ERROR",
                    "field": None,
                }
            ]
        }
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Todo App"}

app.include_router(UserRouter)
app.include_router(TaskRouter)

