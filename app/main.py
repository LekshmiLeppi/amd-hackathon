
from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.validate import router as validate_router
from app.api.report import router as report_router

app=FastAPI(
    title="Audit Compliance Validator"
)

app.include_router(
    report_router,
    tags=["Reports"]
)
app.include_router(
    health_router,
    tags=["Health"]
)

app.include_router(
    upload_router,
    tags=["Upload"]
)

app.include_router(
    validate_router,
    tags=["Validation"]
)
