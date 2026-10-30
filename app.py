
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
from pathlib import Path
from services.whatsapp import simular_envio
from flask import flash 
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

CAMINHO_BANCO = Path("data") / "clientes.db"


def conectar_banco():

    try:
        conexao = sqlite3.connect(CAMINHO_BANCO)
        conexao.row_factory = sqlite3.Row
        return conexao
    except sqlite3.Error as erro:
        print(f"Erro ao conectao ao banco de dados: {erro}")
        raise

@app.route("/")
def listar_clientes():
    trilha_filtro = request.args.get("trilha", "")

    with conectar_banco() as conexao:
        if trilha_filtro:
            clientes = conexao.execute("""
                SELECT DISTINCT
                    c.*,
                    ts.trilha
                FROM clientes c
                JOIN trilhas_sugeridas ts
                    ON c.id = ts.cliente_id
                WHERE ts.trilha = ?
                ORDER BY c.nome_completo
            """, (trilha_filtro,)).fetchall()
        else:
            clientes = conexao.execute("""
                SELECT *
                FROM clientes
                ORDER BY nome_completo
            """).fetchall()

    return render_template(
        "clientes.html",
        clientes=clientes,
        trilha_filtro=trilha_filtro
    )



@app.route("/cliente/<int:cliente_id>")
def detalhes_cliente(cliente_id):
    with conectar_banco() as conexao:
        cliente = conexao.execute("""
            SELECT *
            FROM clientes
            WHERE id = ?
        """, (cliente_id,)).fetchone()

        if cliente is None:
            return "Cliente não encontrado", 404

        trilhas = conexao.execute("""
            SELECT trilha, motivo, prioridade
            FROM trilhas_sugeridas
            WHERE cliente_id = ?
            ORDER BY prioridade
        """, (cliente_id,)).fetchall()


        trilhas_confirmadas = conexao.execute("""
            SELECT trilha
            FROM trilhas_confirmadas
            WHERE cliente_id = ?
        """, (cliente_id,)).fetchall()

        decisao = conexao.execute("""
            SELECT confirmado
            FROM decisoes_cliente
            WHERE cliente_id = ?
        """, (cliente_id,)).fetchone()



    return render_template(
        "detalhes.html",
        cliente=cliente,
        trilhas=trilhas,
        trilhas_confirmadas=trilhas_confirmadas,
        decisao=decisao
    )


@app.route("/cliente/<int:cliente_id>/confirmar", methods=["POST"])
def confirmar_trilhas(cliente_id):
    trilhas_escolhidas = request.form.getlist("trilhas")

    trilhas_validas = {
        "Alto valor",
        "Compra em quantidade",
        "Incentivo",
        "Público jovem",
        "Geral"
    }

    if not set(trilhas_escolhidas).issubset(trilhas_validas):
        return "Trilha inválida", 400

    with conectar_banco() as conexao:
        cliente = conexao.execute(
            "SELECT id FROM clientes WHERE id = ?",
            (cliente_id,)
        ).fetchone()

        if cliente is None:
            return "Cliente não encontrado", 404

        conexao.execute("""
            DELETE FROM trilhas_confirmadas
            WHERE cliente_id = ?
        """, (cliente_id,))

        for trilha in trilhas_escolhidas:
            conexao.execute("""
                INSERT INTO trilhas_confirmadas (cliente_id, trilha)
                VALUES (?, ?)
            """, (cliente_id, trilha))

        conexao.execute("""
            INSERT INTO decisoes_cliente (cliente_id, confirmado, atualizado_em)
            VALUES (?, 1, ?)
            ON CONFLICT(cliente_id) DO UPDATE SET
                confirmado = 1,
                atualizado_em = excluded.atualizado_em
        """, (cliente_id, datetime.now().isoformat(timespec="seconds")))

    return redirect(url_for("detalhes_cliente", cliente_id=cliente_id))



@app.route("/agendamentos")
def listar_agendamentos():
    with conectar_banco() as conexao:
        agendamentos = conexao.execute("""
            SELECT
                a.id,
                a.cliente_id,
                c.nome_completo,
                c.telefone,
                a.trilha,
                a.numero_mensagem,
                a.mensagem,
                a.data_envio,
                a.status
            FROM agendamentos a
            JOIN clientes c ON c.id = a.cliente_id
            ORDER BY a.data_envio, a.cliente_id
        """).fetchall()

    return render_template(
        "agendamentos.html",
        agendamentos=agendamentos
    )


@app.route("/simular-envio/<int:agendamento_id>", methods=["POST"])
def executar_simulacao(agendamento_id):
    try:
        resultado = simular_envio(agendamento_id)
        flash(resultado["status"])
    except ValueError as erro:
        flash(str(erro))

    return redirect(url_for("listar_agendamentos"))


@app.route("/historico")
def listar_historico():
    with conectar_banco() as conexao:
        historico = conexao.execute("""
            SELECT
                h.*,
                c.nome_completo,
                a.trilha,
                a.numero_mensagem
            FROM historico_envios h
            JOIN clientes c ON c.id = h.cliente_id
            JOIN agendamentos a ON a.id = h.agendamento_id
            ORDER BY h.data_simulacao DESC
        """).fetchall()

    return render_template(
        "historico.html",
        historico=historico
    )

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404


@app.errorhandler(500)
def erro_interno(erro):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
