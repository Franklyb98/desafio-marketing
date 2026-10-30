
import sqlite3
from pathlib import Path


CAMINHO_BANCO = Path("data") / "clientes.db"


TRILHAS = {
    "Alto valor": 1,
    "Compra em quantidade": 2,
    "Incentivo": 3,
    "Público jovem": 4,
    "Geral": 5,
}


def formatar_reais(valor):
    valor_formatado = f"{valor:,.2f}"
    valor_formatado = valor_formatado.replace(",", "X")
    valor_formatado = valor_formatado.replace(".", ",")
    valor_formatado = valor_formatado.replace("X", ".")
    return f"R$ {valor_formatado}"


def classificar_cliente(cliente):
    trilhas = []

    valor = cliente["valor_total_carrinhos"]
    itens = cliente["quantidade_total_itens"]
    idade = cliente["idade"]

    if valor >= 10000:
        trilhas.append((
            "Alto valor",
            f"Valor total {formatar_reais(valor)} >= R$ 10.000,00"
        ))

    if itens >= 15:
        trilhas.append((
            "Compra em quantidade",
            f"Quantidade total de itens {itens} >= 15"
        ))

    if valor < 1000:
        trilhas.append((
            "Incentivo",
            f"Valor total {formatar_reais(valor)} < R$ 1.000,00"
        ))

    if idade is not None and idade < 30:
        trilhas.append((
            "Público jovem",
            f"Idade {idade} < 30 anos"
        ))

    if not trilhas:
        trilhas.append((
            "Geral",
            "Não se encaixou em nenhuma das outras trilhas"
        ))

    return trilhas


def salvar_classificacoes():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row

    try:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS trilhas_sugeridas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                trilha TEXT NOT NULL,
                motivo TEXT NOT NULL,
                prioridade INTEGER NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes(id),
                UNIQUE (cliente_id, trilha)
            )
        """)

        clientes = conexao.execute("""
            SELECT
                id,
                valor_total_carrinhos,
                quantidade_total_itens,
                idade
            FROM clientes
        """).fetchall()

        conexao.execute("DELETE FROM trilhas_sugeridas")

        for cliente in clientes:
            sugestoes = classificar_cliente(cliente)

            for trilha, motivo in sugestoes:
                conexao.execute("""
                    INSERT INTO trilhas_sugeridas (
                        cliente_id,
                        trilha,
                        motivo,
                        prioridade
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    cliente["id"],
                    trilha,
                    motivo,
                    TRILHAS[trilha]
                ))

        conexao.commit()
        print(f"Clientes classificados: {len(clientes)}")

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()


if __name__ == "__main__":
    salvar_classificacoes()
