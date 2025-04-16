from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.reader_excel import reader_excel

router = APIRouter()


@router.post("/upload-investments-read")
async def upload_investments(file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser .xlsx")

    content = await file.read()
    data = reader_excel(content)

    return {"data": data}


@router.post("/upload-investments")
async def upload_investments(file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser .xlsx")

    content = await file.read()
    data = reader_excel(content)

    return {"data": data}
