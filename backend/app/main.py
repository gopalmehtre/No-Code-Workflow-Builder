from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import json

from app.database import engine, Base
from app.api.routes import documents, workflow, chat
from app.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    description="No-Code Workflow Builder API",
    version="1.0.0",
    debug=settings.debug
)

try:
    origins = json.loads(settings.allowed_origins)
except:
    origins = ["http://localhost:3000", "http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api")
app.include_router(workflow.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "FlowAI Studio API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting")
    logger.info(f"Database URL: {settings.database_url}")
    logger.info(f"CORS Origins: {origins}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")

if __name__=="__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )