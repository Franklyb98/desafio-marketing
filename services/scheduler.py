
import sqlite3
from pathlib import Path
from datetime import date, timedelta
from services.messages import MENSAGENS
import os
from dotenv import load_dotenv

load_dotenv()

DIA_ENVIO = int(os.getenv("DIA_ENVIO", "0"))

CAMINHO_BANCO = Path("data") / "clientes.db"


PRIORIDADES = {
    "Alto valor": 1,
    "Compra em quantidade": 2,
    "Incentivo": 3,
    "Público jovem": 4,
    "Geral": 5
}


def proxima_data_envio():
    hoje = date.today()
    dias_ate_envio = (DIA_ENVIO - hoje.weekday()) % 7

    if dias_ate_envio == 0:
        dias_ate_envio = 7

    return hoje + timedelta(days=dias_ate_envio)


def criar_tabela_agendamentos(conexao):
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            trilha TEXT NOT NULL,
            numero_mensagem INTEGER NOT NULL,
            mensagem TEXT NOT NULL,
            data_envio TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pendente',
            FOREIGN KEY (cliente_id) REFERENCES clientes(id),
            UNIQUE (cliente_id, trilha, numero_mensagem)
        )
    """)


def gerar_agendamentos():
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        conexao.row_factory = sqlite3.Row
        criar_tabela_agendamentos(conexao)

        clientes = conexao.execute("""
            SELECT c.id, c.nome_completo
            FROM clientes c
            JOIN decisoes_cliente d
                ON c.id = d.cliente_id
            WHERE d.confirmado = 1
            ORDER BY c.id
        """).fetchall()

        data_inicial = proxima_data_envio()

        agendamentos_existentes = conexao.execute("""
            SELECT cliente_id, trilha, numero_mensagem
            FROM agendamentos
        """).fetchall()

        existentes = {
            (item["cliente_id"], item["trilha"], item["numero_mensagem"])
            for item in agendamentos_existentes
            }
         

        for cliente in clientes:
            trilhas = conexao.execute("""
                SELECT trilha
                FROM trilhas_confirmadas
                WHERE cliente_id = ?
            """, (cliente["id"],)).fetchall()

            trilhas_ordenadas = sorted(
                [item["trilha"] for item in trilhas],
                key=lambda trilha: PRIORIDADES[trilha]
            )

            semana = 0

            primeiro_nome = cliente["nome_completo"].split()[0]

            for trilha in trilhas_ordenadas:
                for numero, texto in enumerate(MENSAGENS[trilha], start=1):

                    chave = (cliente["id"], trilha, numero)

                    if chave in existentes:
                        semana += 1
                        continue

                    mensagem = texto.replace("{nome}", primeiro_nome)

                    data_envio = (
                        data_inicial + timedelta(weeks=semana)
                    ).isoformat()

                    conexao.execute("""
                        INSERT  INTO agendamentos (
                            cliente_id,
                            trilha,
                            numero_mensagem,
                            mensagem,
                            data_envio
                        )
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        cliente["id"],
                        trilha,
                        numero,
                        mensagem,
                        data_envio
                    ))

                    semana += 1

        total = conexao.execute("""
            SELECT COUNT(*) FROM agendamentos
        """).fetchone()[0]

        print(f"Agendamentos registrados: {total}")


if __name__ == "__main__":
    gerar_agendamentos()
