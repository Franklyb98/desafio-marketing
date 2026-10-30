from services.classification import classificar_cliente


def test_cliente_alto_valor():
    cliente = {
        "valor_total_carrinhos": 12000,
        "quantidade_total_itens": 5,
        "idade": 35
    }

    resultado = classificar_cliente(cliente)

    assert resultado[0][0] == "Alto valor"


def test_cliente_compra_quantidade():
    cliente = {
        "valor_total_carrinhos": 2000,
        "quantidade_total_itens": 20,
        "idade": 35
    }

    resultado = classificar_cliente(cliente)

    assert resultado[0][0] == "Compra em quantidade"


def test_cliente_incentivo():
    cliente = {
        "valor_total_carrinhos": 500,
        "quantidade_total_itens": 5,
        "idade": 35
    }

    resultado = classificar_cliente(cliente)

    assert resultado[0][0] == "Incentivo"


def test_cliente_publico_jovem():
    cliente = {
        "valor_total_carrinhos": 2000,
        "quantidade_total_itens": 5,
        "idade": 25
    }

    resultado = classificar_cliente(cliente)

    assert resultado[0][0] == "Público jovem"


def test_cliente_geral():
    cliente = {
        "valor_total_carrinhos": 2000,
        "quantidade_total_itens": 5,
        "idade": 35
    }

    resultado = classificar_cliente(cliente)

    assert resultado[0][0] == "Geral"

def test_cliente_pode_ter_multiplas_trilhas():
    cliente = {
        "valor_total_carrinhos": 12000,
        "quantidade_total_itens": 20,
        "idade": 25
    }

    resultado = classificar_cliente(cliente)

    nomes_trilhas = [trilha[0] for trilha in resultado]

    assert "Alto valor" in nomes_trilhas
    assert "Compra em quantidade" in nomes_trilhas
    assert "Público jovem" in nomes_trilhas
    assert len(resultado) == 3

    