from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.validate import router as validate_router
from app.api.report import router as report_router

app = FastAPI(
    title="Audit Compliance Validator",
    version="1.0.0"
)

# ----------------------------
# CORS (IMPORTANT FOR STREAMLIT)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# ROOT (DEBUG)
# ----------------------------
@app.get("/")
def root():
    return {"status": "running"}

# ----------------------------
# ROUTERS (IMPORTANT FIX)
# ----------------------------
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(upload_router, prefix="/upload", tags=["Upload"])

# ✅ IMPORTANT: ONLY ONE PREFIX
app.include_router(validate_router, prefix="/validate", tags=["Validation"])

app.include_router(report_router, prefix="/report", tags=["Reports"])