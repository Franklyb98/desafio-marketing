import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path("data") / "clientes.db"


def criar_tabelas_decisoes():
    with sqlite3.connect(CAMINHO_BANCO) as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS decisoes_cliente (
                cliente_id INTEGER PRIMARY KEY,
                confirmado INTEGER NOT NULL DEFAULT 0,
                atualizado_em TEXT,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS trilhas_confirmadas (
                cliente_id INTEGER NOT NULL,
                trilha TEXT NOT NULL,
                PRIMARY KEY (cliente_id, trilha),
                FOREIGN KEY (cliente_id) REFERENCES clientes(id)
            )
        """)

    print("Tabelas de decisões criadas com sucesso!")


if __name__ == "__main__":
    criar_tabelas_decisoes()