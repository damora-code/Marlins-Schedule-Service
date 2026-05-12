from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Marlins Schedule Service",
    description="Service for retrieving Miami Marlins and affiliate schedule information.",
    version="1.0.0",
)

app.include_router(router)