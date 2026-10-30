
import sqlite3
import json
from pathlib import Path
from collections import defaultdict
from contextlib import closing


CAMINHO_BANCO = Path("data") / "clientes.db"
PASTA_RAW = Path("data") / "raw"


def conectar_banco():
    CAMINHO_BANCO.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(CAMINHO_BANCO)


def criar_tabela_clientes():
    with closing(conectar_banco()) as conexao:
        with conexao:
            conexao.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY,
                    nome_completo TEXT NOT NULL,
                    idade INTEGER,
                    sexo TEXT,
                    estado TEXT,
                    telefone TEXT,
                    valor_total_carrinhos REAL DEFAULT 0,
                    quantidade_total_itens INTEGER DEFAULT 0
                )
            """)



def localizar_arquivos():
    if not PASTA_RAW.exists():
        raise FileNotFoundError(
            "A pasta data/raw não foi encontrada. Execute primeiro extraction.py."
        )

    pastas = sorted(
        (pasta for pasta in PASTA_RAW.iterdir() if pasta.is_dir()),
        reverse=True
    )

    for pasta in pastas:
        arquivos_clientes = {
            arquivo.stem.removeprefix("clientes_"): arquivo
            for arquivo in pasta.glob("clientes_*.json")
        }

        arquivos_carrinhos = {
            arquivo.stem.removeprefix("carrinhos_"): arquivo
            for arquivo in pasta.glob("carrinhos_*.json")
        }

        horarios_comuns = sorted(
            set(arquivos_clientes) & set(arquivos_carrinhos),
            reverse=True
        )

        if horarios_comuns:
            horario = horarios_comuns[0]

            return (
                arquivos_clientes[horario],
                arquivos_carrinhos[horario]
            )

    raise FileNotFoundError(
        "Não foram encontrados arquivos de clientes e carrinhos "
        "com o mesmo horário em data/raw."
    )


def carregar_json(caminho):
    with caminho.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def consolidar_carrinhos(carrinhos):
    totais = defaultdict(lambda: {"valor": 0.0, "itens": 0})

    for carrinho in carrinhos:
        user_id = carrinho["userId"]
        totais[user_id]["valor"] += carrinho["total"]
        totais[user_id]["itens"] += carrinho["totalQuantity"]

    return totais


def inserir_clientes(clientes, totais):
    with closing(conectar_banco()) as conexao:
        with conexao:
            for cliente in clientes:
                user_id = cliente["id"]
                total = totais[user_id]

                nome_completo = (
                    f"{cliente['firstName']} "
                    f"{cliente['lastName']}"
                )

                conexao.execute("""
                    INSERT INTO clientes (
                        id, nome_completo, idade, sexo, estado, telefone,
                        valor_total_carrinhos, quantidade_total_itens
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        nome_completo = excluded.nome_completo,
                        idade = excluded.idade,
                        sexo = excluded.sexo,
                        estado = excluded.estado,
                        telefone = excluded.telefone,
                        valor_total_carrinhos = excluded.valor_total_carrinhos,
                        quantidade_total_itens = excluded.quantidade_total_itens
                """, (
                    user_id,
                    nome_completo,
                    cliente.get("age"),
                    cliente.get("gender"),
                    cliente.get("address", {}).get("state"),
                    cliente.get("phone"),
                    total["valor"],
                    total["itens"]
                ))


def main():
    criar_tabela_clientes()

    arquivo_clientes, arquivo_carrinhos = localizar_arquivos()

    dados_clientes = carregar_json(arquivo_clientes)
    dados_carrinhos = carregar_json(arquivo_carrinhos)

    totais = consolidar_carrinhos(dados_carrinhos["carts"])

    inserir_clientes(dados_clientes["users"], totais)

    with closing(conectar_banco()) as conexao:
        with conexao:
            quantidade = conexao.execute(
                "SELECT COUNT(*) FROM clientes"
            ).fetchone()[0]

    print(f"Clientes cadastrados no banco: {quantidade}")


if __name__ == "__main__":
    main()
