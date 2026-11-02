import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from .database import engine, get_db
from .model import Base, Institution
from .rag_chatbot import ask_school_chatbot
from .schemas import (
    ChatRequest,
    ChatResponse,
    InstitutionCreate,
    InstitutionResponse,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creates missing tables. It does not alter existing table columns.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="InstitutionAI API",
    description="Institution management and institution-specific RAG chatbot API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

@app.get("/")
def home():
    return {"message": "InstitutionAI API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/institutions", response_model=InstitutionResponse, status_code=201)
def create_institution(data: InstitutionCreate, db: Session = Depends(get_db)):
    if data.email:
        existing = db.scalar(
            select(Institution).where(Institution.email == data.email)
        )
        if existing:
            raise HTTPException(status_code=409, detail="Email already registered")

    institution = Institution(
        name=data.name,
        institution_type=data.institution_type,
        email=data.email,
    )
    try:
        db.add(institution)
        db.commit()
        db.refresh(institution)
        return institution
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Institution could not be created due to a duplicate value")
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Database error while creating institution")
        raise HTTPException(status_code=500, detail="Database operation failed")

@app.get("/institutions/{institution_id}", response_model=InstitutionResponse)
def get_institution(institution_id: int, db: Session = Depends(get_db)):
    institution = db.get(Institution, institution_id)
    if institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")
    return institution

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    question = request.question.strip()
    institution_id = request.institution_id.strip()
    try:
        answer = ask_school_chatbot(
            question=question,
            institution_id=institution_id,
        )
        return ChatResponse(
            institution_id=institution_id,
            question=question,
            answer=answer,
        )
    except Exception:
        logger.exception("Failed to process chatbot request")
        raise HTTPException(
            status_code=500,
            detail="The chatbot encountered an error. Please try again.",
        )
