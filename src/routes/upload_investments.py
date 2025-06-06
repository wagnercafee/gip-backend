import asyncio
from fastapi import APIRouter, UploadFile, File
from src.services.reader_excel import process_excel_file
from src.services.investments import insert_investments, remove_duplicates, investments, calc_proventos

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

@router.get("/proventos")
async def proventos_route():
    tipos_a_buscar = {
        "dividendos": "Dividendo",
        "jcp": "Juros Sobre Capital Próprio",
        "rendimentos": "Rendimento",
        "leilao_de_fracoes": "Leilão de Fração"
    }

    tasks = [calc_proventos(tipo) for tipo in tipos_a_buscar.values()]

    resultados_lista = await asyncio.gather(*tasks)

    resposta_final = dict(zip(tipos_a_buscar.keys(), resultados_lista))

    return resposta_final