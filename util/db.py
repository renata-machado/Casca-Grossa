import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def obter_conexao():
    conn = sqlite3.connect(BASE_DIR / "dados.db")
    conn.row_factory = sqlite3.Row
    return conn