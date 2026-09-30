import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

load_dotenv("settings.env")
load_dotenv()

from app.models import RealityRequest, RealityResponse
from app.services import GENERATED_IMAGES_DIRECTORY, generate_alternate_reality


GENERATED_IMAGES_DIRECTORY.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="PARACOSM Backend", version="1.0.0")
origins = [
    origin.strip()
    for origin in os.getenv(
        "CLIENT_ORIGINS",
        "http://localhost:5173,http://localhost:5174,null",
    ).split(",")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/generated", StaticFiles(directory=GENERATED_IMAGES_DIRECTORY), name="generated")


@app.get("/api/health")
async def health():
    return {"ok": True, "service": "paracosm-python-backend"}


async def create_reality(payload: RealityRequest, request: Request):
    public_url = os.getenv("PUBLIC_SERVER_URL") or str(request.base_url).rstrip("/")
    return await generate_alternate_reality(payload.prompt, public_url)


@app.post("/api/generate-reality", response_model=RealityResponse)
async def generate_reality(payload: RealityRequest, request: Request):
    return await create_reality(payload, request)


@app.post("/api/reality/generate", response_model=RealityResponse)
async def generate_reality_compatibility(payload: RealityRequest, request: Request):
    return await create_reality(payload, request)


@app.exception_handler(Exception)
async def unexpected_error(_request: Request, error: Exception):
    print(error)
    return JSONResponse(
        status_code=500,
        content={"error": str(error) or "Unexpected server error."},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8080")),
        reload=True,
    )
