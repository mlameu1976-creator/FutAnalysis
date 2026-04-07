from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.opportunities import router as opportunities_router
from app.api.routes.predictions import router as predictions_router

from app.api.routes.internal_generate_pipeline import router as pipeline_router


app = FastAPI(title="FutAnalysis API")


# CORS — permitir acesso do frontend
origins = [
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# rotas públicas
app.include_router(opportunities_router)
app.include_router(predictions_router)

# rotas internas
app.include_router(pipeline_router)