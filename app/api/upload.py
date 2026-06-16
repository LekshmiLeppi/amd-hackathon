
from fastapi import APIRouter, UploadFile, File

from app.services.file_service import FileService
from app.services.document_parser import DocumentParser
from app.config.settings import settings

router=APIRouter()

@router.post("/upload")
async def upload_document(
    file:UploadFile=File(...)
):

    path=FileService.save_file(
        file,
        settings.UPLOAD_DIR
    )

    text=DocumentParser.parse(path)

    return {
        "file":file.filename,
        "characters":len(text),
        "preview":text[:500]
    }
