
import json
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BOTMAKER_ACCESS_TOKEN = os.getenv("BOTMAKER_ACCESS_TOKEN")
BOTMAKER_CHANNEL_ID = os.getenv("BOTMAKER_CHANNEL_ID")
BOTMAKER_INTENT_NAME = os.getenv("BOTMAKER_INTENT_NAME")

CAMINHO_BANCO = Path("data") / "clientes.db"

ENDPOINT = "https://api.botmaker.com/v2.0/notifications"


def formatar_telefone(telefone):
    original = str(telefone).strip()
    numeros = re.sub(r"\D", "", original)

    if original.startswith("+"):
        return numeros

    if numeros.startswith("00"):
        return numeros[2:]

    if not numeros.startswith("55"):
        return "55" + numeros

    return numeros


def simular_envio(agendamento_id):
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        conexao.row_factory = sqlite3.Row

        agendamento = conexao.execute("""
            SELECT
                a.*,
                c.nome_completo,
                c.telefone,
                d.confirmado
            FROM agendamentos a
            JOIN clientes c ON c.id = a.cliente_id
            JOIN decisoes_cliente d ON d.cliente_id = c.id
            WHERE a.id = ?
        """, (agendamento_id,)).fetchone()

        if not agendamento:
            raise ValueError("Agendamento não encontrado.")

        if not agendamento["confirmado"]:
            raise ValueError("O cliente não foi confirmado pelo analista.")

        if agendamento["status"] != "Pendente":
            raise ValueError("Este agendamento não está pendente.")

        telefone = formatar_telefone(agendamento["telefone"])
        primeiro_nome = agendamento["nome_completo"].split()[0]

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "access-token": BOTMAKER_ACCESS_TOKEN or "TOKEN_NAO_CONFIGURADO"
        }

        body = {
            "name": f"Marketing - {agendamento['trilha']}",
            "channelId": BOTMAKER_CHANNEL_ID or "CANAL_NAO_CONFIGURADO",
            "intentIdOrName": BOTMAKER_INTENT_NAME or "INTENT_NAO_CONFIGURADO",
            "contacts": [
                {
                    "contactId": telefone,
                    "variables": {
                        "nome": primeiro_nome,
                        "mensagem": agendamento["mensagem"]
                    }
                }
            ]
        }

        conexao.execute("""
            INSERT INTO historico_envios (
                agendamento_id,
                cliente_id,
                mensagem,
                telefone,
                data_simulacao,
                endpoint,
                metodo,
                headers_json,
                body_json,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            agendamento_id,
            agendamento["cliente_id"],
            agendamento["mensagem"],
            telefone,
            datetime.now().isoformat(timespec="seconds"),
            ENDPOINT,
            "POST",
            json.dumps(headers, ensure_ascii=False),
            json.dumps(body, ensure_ascii=False),
            "Simulado - não enviado"
        ))

        conexao.execute("""
            UPDATE agendamentos
            SET status = 'Simulado'
            WHERE id = ?
        """, (agendamento_id,))

    return {
        "endpoint": ENDPOINT,
        "metodo": "POST",
        "headers": headers,
        "body": body,
        "status": "Simulado - não enviado"
    }
