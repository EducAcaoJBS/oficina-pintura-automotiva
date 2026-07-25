"""
Camada de acesso a dados (SQLite).
Responsável por criar tabelas e expor funções CRUD
para leads, agendamentos, portfólio e depoimentos.
"""
import sqlite3
from datetime import datetime

DB_NAME = "oficina.db"


def get_conn():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, telefone TEXT, servico TEXT,
            veiculo TEXT, estado_veiculo TEXT,
            mensagem TEXT, status TEXT DEFAULT 'Pendente',
            criado_em TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT, telefone TEXT, endereco TEXT,
            data_preferida TEXT, hora_preferida TEXT,
            observacoes TEXT, criado_em TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT, descricao TEXT,
            caminho_imagem TEXT, criado_em TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS depoimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT, nota INTEGER, comentario TEXT,
            criado_em TEXT
        )
    """)

    # Depoimentos de exemplo (seed) — só insere se tabela vazia
    cur.execute("SELECT COUNT(*) FROM depoimentos")
    if cur.fetchone()[0] == 0:
        seed = [
            ("Carlos Silva", 5, "Serviço impecável, carro saiu novo!"),
            ("Marina Costa", 5, "Atendimento no local foi um diferencial enorme."),
            ("Rafael Souza", 4, "Ótimo acabamento, recomendo demais."),
        ]
        cur.executemany(
            "INSERT INTO depoimentos (nome_cliente, nota, comentario, criado_em) VALUES (?,?,?,?)",
            [(n, no, c, datetime.now().isoformat()) for n, no, c in seed]
        )

    conn.commit()
    conn.close()


# ---------- LEADS ----------
def add_lead(nome, telefone, servico, veiculo, estado_veiculo, mensagem):
    conn = get_conn()
    conn.execute("""
        INSERT INTO leads (nome, telefone, servico, veiculo, estado_veiculo, mensagem, criado_em)
        VALUES (?,?,?,?,?,?,?)
    """, (nome, telefone, servico, veiculo, estado_veiculo, mensagem, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_leads():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM leads ORDER BY criado_em DESC").fetchall()
    conn.close()
    return rows


def update_lead_status(lead_id, status):
    conn = get_conn()
    conn.execute("UPDATE leads SET status=? WHERE id=?", (status, lead_id))
    conn.commit()
    conn.close()


def delete_lead(lead_id):
    conn = get_conn()
    conn.execute("DELETE FROM leads WHERE id=?", (lead_id,))
    conn.commit()
    conn.close()


# ---------- AGENDAMENTOS ----------
def add_agendamento(nome, telefone, endereco, data_preferida, hora_preferida, observacoes):
    conn = get_conn()
    conn.execute("""
        INSERT INTO agendamentos (nome, telefone, endereco, data_preferida, hora_preferida, observacoes, criado_em)
        VALUES (?,?,?,?,?,?,?)
    """, (nome, telefone, endereco, str(data_preferida), str(hora_preferida), observacoes, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_agendamentos():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM agendamentos ORDER BY criado_em DESC").fetchall()
    conn.close()
    return rows


# ---------- PORTFOLIO ----------
def add_portfolio_item(titulo, descricao, caminho_imagem):
    conn = get_conn()
    conn.execute("""
        INSERT INTO portfolio (titulo, descricao, caminho_imagem, criado_em)
        VALUES (?,?,?,?)
    """, (titulo, descricao, caminho_imagem, datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_portfolio():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM portfolio ORDER BY criado_em DESC").fetchall()
    conn.close()
    return rows


def delete_portfolio_item(item_id):
    conn = get_conn()
    conn.execute("DELETE FROM portfolio WHERE id=?", (item_id,))
    conn.commit()
    conn.close()


# ---------- DEPOIMENTOS ----------
def get_depoimentos():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM depoimentos ORDER BY criado_em DESC").fetchall()
    conn.close()
    return rows
