from fastapi import APIRouter, HTTPException, UploadFile, File
from src.services.reader_excel import process_excel_file
from src.services.investments import insert_investments, remove_duplicates, calcular_preco_medio_e_lucro

router = APIRouter()


@router.post("/upload-investments")
async def upload_investments(file: UploadFile = File(...)):
    content = await file.read()
    data = process_excel_file(content, file.filename)
    insert = await insert_investments(data)
    duplicates = await remove_duplicates()
    return insert, duplicates


@router.get("/investments/summary")
async def summary():
    result = await calcular_preco_medio_e_lucro()
    return result
