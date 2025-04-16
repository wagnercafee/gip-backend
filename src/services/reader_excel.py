import pandas as pd
from io import BytesIO
from fastapi import HTTPException


def process_excel_file(file_content: bytes, filename: str):
    # Valida o tipo de arquivo
    if not filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser .xlsx")

    # Processa o conteúdo do Excel
    data = reader_excel(file_content)
    return data


# def reader_excel(file_content: bytes):
#     df = pd.read_excel(BytesIO(file_content))
#     return df.to_dict(orient="records")

def reader_excel(file_content: bytes):
    """
    Lê o conteúdo do arquivo Excel, valida as colunas e mapeia para os nomes do banco de dados.
    """
    # Define o mapeamento das colunas do Excel para as colunas do banco de dados
    column_mapping = {
        "Entrada/Saída": "entrada_saida",
        "Data": "data",
        "Movimentação": "movimentacao",
        "Produto": "produto",
        "Instituição": "instituicao",
        "Quantidade": "quantidade",
        "Preço unitário": "preco_unitario",
        "Valor da Operação": "valor_da_operacao",
    }

    # Lê o arquivo Excel
    df = pd.read_excel(BytesIO(file_content))

    # Valida se todas as colunas esperadas estão presentes no Excel
    missing_columns = [col for col in column_mapping if col not in df.columns]
    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Colunas ausentes no arquivo Excel: {', '.join(missing_columns)}"
        )

    # Renomeia as colunas do DataFrame para os nomes do banco de dados
    df = df.rename(columns=column_mapping)

    # Converte a coluna "data" para o formato datetime
    try:
        df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="A coluna 'Data' deve estar no formato DD/MM/AAAA."
        )

    # Retorna os dados como uma lista de dicionários
    return df.to_dict(orient="records")
