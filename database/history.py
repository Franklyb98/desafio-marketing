
import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path("data") / "clientes.db"


def criar_tabela_historico():
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS historico_envios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agendamento_id INTEGER NOT NULL,
                cliente_id INTEGER NOT NULL,
                mensagem TEXT NOT NULL,
                telefone TEXT NOT NULL,
                data_simulacao TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                metodo TEXT NOT NULL,
                headers_json TEXT NOT NULL,
                body_json TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (agendamento_id) REFERENCES agendamentos(id),
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        """)

    print("Tabela de histórico criada com sucesso!")


if __name__ == "__main__":
    criar_tabela_historico()
