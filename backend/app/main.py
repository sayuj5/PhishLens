from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.engine.heuristics import analyze_url

app = FastAPI(
    title="PhishLens API",
    description="Explainable Heuristic Phishing URL Analyzer API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str

@app.post("/api/v1/analyze")
async def analyze(request: AnalyzeRequest):
    result = analyze_url(request.url)
    if "error" in result:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/")
async def root():
    return {"message": "PhishLens API is running. Access /docs for Swagger UI."}
