"""
Módulo de Conexão e Inicialização do Banco de Dados SQLite
"""
import os
import sqlite3
from typing import Generator
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "guardianai.db")

def ensure_data_directory() -> None:
    """Garante que a pasta 'data' exista."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

def init_db() -> None:
    """
    Inicializa o esquema do banco SQLite com tabelas e índices.
    Executado de forma idempotente (CREATE TABLE IF NOT EXISTS).
    """
    ensure_data_directory()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # 1. Tabela de Mensagens do Chat
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensagens_chat (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                pet_id INTEGER,
                sender TEXT NOT NULL,
                text TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mensagens_session ON mensagens_chat (session_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_mensagens_pet ON mensagens_chat (pet_id);")

        # 2. Tabela de Auditoria Clínica de Triagens
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS auditoria_triagens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                pet_id INTEGER,
                nome_pet TEXT,
                pergunta TEXT NOT NULL,
                resposta TEXT NOT NULL,
                categoria TEXT NOT NULL,
                urgencia TEXT NOT NULL,
                origem_resposta TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_auditoria_session ON auditoria_triagens (session_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_auditoria_pet ON auditoria_triagens (pet_id);")

        conn.commit()

@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Fornece uma conexão gerenciada com o banco SQLite.
    Usa row_factory para retorno como dicionário.
    """
    ensure_data_directory()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
