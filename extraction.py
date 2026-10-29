
import requests
import json
from pathlib import Path
from datetime import datetime

URL_USERS = "https://dummyjson.com/users?limit=0"
URL_CARTS = "https://dummyjson.com/carts?limit=0"


def buscar_dados(url):
    resposta = requests.get(url, timeout=30)
    resposta.raise_for_status()
    return resposta.json()


def salvar_json(dados, nome_arquivo, pasta):
    caminho = pasta / nome_arquivo

    with caminho.open("x", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    print(f"Arquivo salvo: {caminho}")


def main():
    agora = datetime.now()
    data = agora.strftime("%Y-%m-%d")
    horario = agora.strftime("%H-%M-%S-%f")

    pasta = Path("data") / "raw" / data
    pasta.mkdir(parents=True, exist_ok=True)

    try:
        clientes = buscar_dados(URL_USERS)
        carrinhos = buscar_dados(URL_CARTS)

        salvar_json(
            clientes,
            f"clientes_{horario}.json",
            pasta
        )

        salvar_json(
            carrinhos,
            f"carrinhos_{horario}.json",
            pasta
        )

        print(f"Clientes encontrados: {len(clientes['users'])}")
        print(f"Carrinhos encontrados: {len(carrinhos['carts'])}")
        print("Extração concluída!")

    except requests.RequestException as erro:
        print(f"Erro ao consultar a API: {erro}")

    except (OSError, TypeError, ValueError) as erro:
        print(f"Erro ao salvar ou processar os dados: {erro}")


if __name__ == "__main__":
    main()
