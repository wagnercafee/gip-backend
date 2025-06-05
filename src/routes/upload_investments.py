from fastapi import APIRouter, UploadFile, File
from src.services.reader_excel import process_excel_file
from src.services.investments import insert_investments, remove_duplicates, investments, unique_tickers, dividends, jcp, rendimento

router = APIRouter()

@router.post("/upload-investments")
async def upload_investments(file: UploadFile = File(...)):
    content = await file.read()
    data = process_excel_file(content, file.filename)
    insert = await insert_investments(data)
    duplicates = await remove_duplicates()
    return insert, duplicates


@router.get("/investments")
async def investments_route():
    resp = await investments()
    return resp


@router.get("/unique_tickers")
async def unique_tickers_route():
    resp = await unique_tickers()
    return resp


@router.get("/dividends")
async def dividends_route():
    resp = await dividends()
    return resp

@router.get("/jcp")
async def jcp_route():
    resp = await jcp()
    return resp

@router.get("/rendimentos")
async def rendimento_route():
    resp = await rendimento()
    return resp

