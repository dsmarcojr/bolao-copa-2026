import sqlite3
import os
from pytz import timezone
from datetime import datetime

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
os.makedirs(DB_DIR, exist_ok=True)

USUARIOS_DB = os.path.join(DB_DIR, 'usuarios.db')
SELECOES_DB = os.path.join(DB_DIR, 'selecoes.db')
PALPITES_DB = os.path.join(DB_DIR, 'palpites.db')
PARTIDAS_DB = os.path.join(DB_DIR, 'partidas.db')

def init_dbs():
    # 1. usuarios.db
    with sqlite3.connect(USUARIOS_DB) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT 0
            )
        ''')
    
    # 2. selecoes.db
    with sqlite3.connect(SELECOES_DB) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_selecao TEXT UNIQUE NOT NULL
            )
        ''')
        # Insert real teams
        teams = ["Brasil", "Alemanha", "Argentina", "França", "Inglaterra", "Espanha", "Itália", "Holanda", "Croácia", "Portugal"]
        for team in teams:
            try:
                conn.execute('INSERT INTO teams (nome_selecao) VALUES (?)', (team,))
            except sqlite3.IntegrityError:
                pass
                
    # 3. partidas.db
    with sqlite3.connect(PARTIDAS_DB) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                home_team_id INTEGER NOT NULL,
                away_team_id INTEGER NOT NULL,
                data_jogo TEXT NOT NULL,
                horario_jogo TEXT NOT NULL,
                resultado_home INTEGER,
                resultado_away INTEGER
            )
        ''')
        # Seed matches if empty
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM matches")
        if cur.fetchone()[0] == 0:
            today = datetime.now(timezone('America/Sao_Paulo')).strftime('%Y-%m-%d')
            # One match today for testing locking
            conn.execute("INSERT INTO matches (home_team_id, away_team_id, data_jogo, horario_jogo) VALUES (1, 2, ?, '16:00')", (today,))
            # One future match
            conn.execute("INSERT INTO matches (home_team_id, away_team_id, data_jogo, horario_jogo) VALUES (3, 4, '2026-06-15', '16:00')")
            
    # 4. palpites.db
    with sqlite3.connect(PALPITES_DB) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS bets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                match_id INTEGER NOT NULL,
                home_team_id INTEGER NOT NULL,
                away_team_id INTEGER NOT NULL,
                score_home INTEGER NOT NULL,
                score_away INTEGER NOT NULL,
                UNIQUE(user_id, match_id)
            )
        ''')

if __name__ == '__main__':
    init_dbs()
    print("Databases initialized successfully.")
