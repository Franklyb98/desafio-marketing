from datetime import date, timedelta
from services.scheduler import proxima_data_envio

from services.scheduler import PRIORIDADES


def test_prioridade_das_trilhas():
    assert PRIORIDADES["Alto valor"] == 1
    assert PRIORIDADES["Compra em quantidade"] == 2
    assert PRIORIDADES["Incentivo"] == 3
    assert PRIORIDADES["Público jovem"] == 4
    assert PRIORIDADES["Geral"] == 5

    
def test_proxima_data_envio_e_segunda():
    resultado = proxima_data_envio()

    assert resultado.weekday() == 0
    assert resultado > date.today()


def test_ordenacao_das_trilhas():
    trilhas = [
        "Público jovem",
        "Incentivo",
        "Alto valor"
    ]

    resultado = sorted(
        trilhas,
        key=lambda trilha: PRIORIDADES[trilha]
    )

    assert resultado == [
        "Alto valor",
        "Incentivo",
        "Público jovem"
    ]

    