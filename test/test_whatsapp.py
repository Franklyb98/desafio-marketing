import sqlite3
import pytest

from services.whatsapp import simular_envio


@pytest.fixture
def banco_teste(tmp_path, monkeypatch):
    caminho = tmp_path / "teste.db"

    conexao = sqlite3.connect(caminho)

    conexao.executescript("""
        CREATE TABLE clientes (
            id INTEGER PRIMARY KEY,
            nome_completo TEXT,
            telefone TEXT
        );

        CREATE TABLE decisoes_cliente (
            cliente_id INTEGER PRIMARY KEY,
            confirmado INTEGER
        );

        CREATE TABLE agendamentos (
            id INTEGER PRIMARY KEY,
            cliente_id INTEGER,
            trilha TEXT,
            numero_mensagem INTEGER,
            mensagem TEXT,
            data_envio TEXT,
            status TEXT
        );

        CREATE TABLE historico_envios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agendamento_id INTEGER,
            cliente_id INTEGER,
            mensagem TEXT,
            telefone TEXT,
            data_simulacao TEXT,
            endpoint TEXT,
            metodo TEXT,
            headers_json TEXT,
            body_json TEXT,
            status TEXT
        );

        INSERT INTO clientes VALUES (1, 'João Silva', '11987654321');
        INSERT INTO decisoes_cliente VALUES (1, 1);
        INSERT INTO agendamentos VALUES (
            1, 1, 'Alto valor', 1,
            'Olá, João!', '2026-11-02', 'Pendente'
        );
    """)

    conexao.commit()
    conexao.close()

    monkeypatch.setattr(
        "services.whatsapp.CAMINHO_BANCO",
        caminho
    )

    return caminho


def test_agendamento_inexistente(banco_teste):
    with pytest.raises(ValueError, match="Agendamento não encontrado"):
        simular_envio(999)


def test_cliente_nao_confirmado(banco_teste):
    with sqlite3.connect(banco_teste) as conexao:
        conexao.execute(
            "UPDATE decisoes_cliente SET confirmado = 0 WHERE cliente_id = 1"
        )

    with pytest.raises(ValueError, match="não foi confirmado"):
        simular_envio(1)


def test_agendamento_ja_simulado(banco_teste):
    with sqlite3.connect(banco_teste) as conexao:
        conexao.execute(
            "UPDATE agendamentos SET status = 'Simulado' WHERE id = 1"
        )

    with pytest.raises(ValueError, match="não está pendente"):
        simular_envio(1)