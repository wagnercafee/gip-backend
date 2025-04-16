from fastapi import APIRouter, UploadFile, File
from src.services.reader_excel import process_excel_file

router = APIRouter()


@router.post("/upload-investments")
async def upload_investments(file: UploadFile = File(...)):
    content = await file.read()
    data = process_excel_file(content, file.filename)
    return {"data": data}
