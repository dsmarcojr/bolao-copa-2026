import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'bolao.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    
    # Tabela de Jogos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jogos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_1 TEXT NOT NULL,
            time_2 TEXT NOT NULL,
            data_hora DATETIME
        )
    ''')
    
    # Tabela de Palpites
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS palpites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            jogo_id INTEGER NOT NULL,
            placar_1 INTEGER NOT NULL,
            placar_2 INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
            FOREIGN KEY (jogo_id) REFERENCES jogos (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(nome, usuario, senha):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (nome, usuario, senha) VALUES (?, ?, ?)', (nome, usuario, senha))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def verify_user(usuario, senha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome FROM usuarios WHERE usuario = ? AND senha = ?', (usuario, senha))
    user = cursor.fetchone()
    conn.close()
    return user # Retorna (id, nome) se encontrado, senão None

def add_palpite(usuario_id, jogo_id, placar_1, placar_2):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO palpites (usuario_id, jogo_id, placar_1, placar_2)
        VALUES (?, ?, ?, ?)
    ''', (usuario_id, jogo_id, placar_1, placar_2))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    users = cursor.fetchall()
    conn.close()
    return users

def get_all_palpites():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, u.nome, j.time_1, j.time_2, p.placar_1, p.placar_2
        FROM palpites p
        JOIN usuarios u ON p.usuario_id = u.id
        JOIN jogos j ON p.jogo_id = j.id
    ''')
    palpites = cursor.fetchall()
    conn.close()
    return palpites

if __name__ == "__main__":
    init_db()
    print("Banco de dados inicializado em:", os.path.abspath(DB_PATH))
