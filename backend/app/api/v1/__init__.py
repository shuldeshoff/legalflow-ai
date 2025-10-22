from fastapi import APIRouter
from app.api.v1 import auth, llm, knowledge, documents, integrations, payments

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(llm.router, prefix="/llm", tags=["llm"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["integrations"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])

