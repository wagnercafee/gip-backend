from decimal import Decimal
from fastapi import HTTPException
from typing import List, Dict
from src.database.connection import get_db_connection

async def insert_investments(data: List[Dict]):
    """
    Insere os dados na tabela investments.
    :param data: Lista de dicionários com os dados a serem inseridos.
    """
    query = """
        INSERT INTO investments (
            entrada_saida,
            data,
            movimentacao,
            produto,
            instituicao,
            quantidade,
            preco_unitario,
            valor_da_operacao
        ) VALUES (
            $1, $2, $3, $4, $5, $6, $7, $8
        )
    """
    conn = await get_db_connection()
    try:
        async with conn.transaction():
            for record in data:
                # Trata os valores para garantir que estejam no formato correto
                quantidade = float(record["quantidade"]) if record.get(
                    "quantidade") not in [None, "", "-"] else 0.0
                preco_unitario = float(record["preco_unitario"]) if record.get(
                    "preco_unitario") not in [None, "", "-"] else 0.0
                valor_da_operacao = float(record["valor_da_operacao"]) if record.get(
                    "valor_da_operacao") not in [None, "", "-"] else 0.0

                await conn.execute(
                    query,
                    record["entrada_saida"],
                    record["data"],
                    record["movimentacao"],
                    record["produto"],
                    record["instituicao"],
                    quantidade,
                    preco_unitario,
                    valor_da_operacao
                )
            return {"message": "Registros inseridos com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao inserir dados: {str(e)}"
        )
    finally:
        await conn.close()


async def remove_duplicates():
    """
    Remove registros duplicados da tabela investments.
    Mantém apenas o primeiro registro de cada conjunto de duplicados.
    """
    query = """
        DELETE FROM investments
        WHERE ctid NOT IN (
            SELECT MIN(ctid)
            FROM investments
            GROUP BY entrada_saida, data, movimentacao, produto, instituicao, quantidade, preco_unitario, valor_da_operacao
        )
    """
    conn = await get_db_connection()
    try:
        async with conn.transaction():
            result = await conn.execute(query)
        return {"message": f"Registros duplicados removidos: {result}"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao remover duplicados: {str(e)}"
        )
    finally:
        await conn.close()


async def investments():
    conn = await get_db_connection()
    try:
        rows = await conn.fetch("""
            SELECT * FROM investments ORDER BY data
        """)
        return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar dados: {e}")
    finally:
        await conn.close()


async def unique_tickers():
    conn = await get_db_connection()
    try:
        rows = await conn.fetch("""
            SELECT DISTINCT produto FROM investments
            ORDER BY produto
        """)
        lista = [row['produto'] for row in rows]
        resultado = sorted([
            item.split(" - ")[0] if " - " in item else item
            for item in lista
        ])
        return resultado
    finally:
        await conn.close()


async def get_proventos(tipo_movimentacao: str):
    conn = await get_db_connection()
    try:
        query = "SELECT * FROM investments WHERE movimentacao LIKE $1 ORDER BY data"
        result = await conn.fetch(query, tipo_movimentacao)
        return [dict(row) for row in result]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar dados: {e}")
    finally:
        await conn.close()


async def calc_proventos(tipo_movimentacao: str):
    proventos_data = await get_proventos(tipo_movimentacao)
    tickers = await unique_tickers()
    resultado = {}

    for ticker in tickers:
        soma_operacoes = Decimal('0.0')

        for provento in proventos_data:
            if ticker in provento['produto']:
                soma_operacoes += provento['valor_da_operacao']

        if soma_operacoes > Decimal('0.0'):
            resultado[ticker] = soma_operacoes

    return resultado