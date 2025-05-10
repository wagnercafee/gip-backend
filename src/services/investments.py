from datetime import datetime
from collections import defaultdict
from fastapi import APIRouter, HTTPException
from decimal import Decimal
from collections import deque
from typing import List, Dict
from typing import Dict, List
from fastapi import HTTPException
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


router = APIRouter()


def extrair_ticker(produto: str) -> str:
    if "-" in produto:
        return produto.split("-")[0].strip()
    return None  # Ignorar produtos sem '-'


async def calcular_preco_medio_e_lucro():
    conn = await get_db_connection()
    try:
        rows = await conn.fetch("""
            SELECT entrada_saida, data, movimentacao, produto, quantidade, preco_unitario, valor_da_operacao
            FROM investments
            ORDER BY data
        """)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao buscar dados: {e}")
    finally:
        await conn.close()

    ativos = defaultdict(lambda: {
        "total_comprado": 0.0,
        "total_vendido": 0.0,
        "quantidade_atual": 0,
        "preco_medio": 0.0,
        "lucro_prejuizo": 0.0,
        "compras": [],
        "vendas": []
    })

    for row in rows:
        ticker = extrair_ticker(row["produto"])
        if not ticker:
            continue  # pula produtos inválidos

        data = row["data"]
        quantidade = float(row["quantidade"])
        preco = float(row["preco_unitario"])
        valor = float(row["valor_da_operacao"])
        entrada_saida = row["entrada_saida"].lower()
        movimentacao = row["movimentacao"].lower()

        ativo = ativos[ticker]

        if entrada_saida == "credito" and "transferência - liquidação" in movimentacao:
            # Compra
            ativo["total_comprado"] += valor
            ativo["quantidade_atual"] += quantidade

            # Recalcular preço médio
            if ativo["quantidade_atual"] != 0:
                ativo["preco_medio"] = ativo["total_comprado"] / \
                    ativo["quantidade_atual"]

            ativo["compras"].append({
                "quantidade": quantidade,
                "valor": valor,
                "data": data.strftime("%Y-%m-%d")
            })

        elif entrada_saida == "debito" and "transferência - liquidação" in movimentacao:
            # Venda
            ativo["total_vendido"] += valor
            ativo["quantidade_atual"] -= quantidade

            lucro_unitario = preco - ativo["preco_medio"]
            lucro_total = lucro_unitario * quantidade
            ativo["lucro_prejuizo"] += lucro_total

            ativo["vendas"].append({
                "quantidade": quantidade,
                "valor": valor,
                "data": data.strftime("%Y-%m-%d"),
                "lucro_prejuizo": round(lucro_total, 2)
            })

    return {"ativos": ativos}
