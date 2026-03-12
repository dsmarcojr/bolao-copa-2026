import sqlite3
import os

DB_DIR = os.path.dirname(__file__)
USERS_DB_PATH = os.path.join(DB_DIR, '..', 'usuarios.db')
PALPITES_DB_PATH = os.path.join(DB_DIR, '..', 'palpites.db')

def get_users_connection():
    return sqlite3.connect(USERS_DB_PATH)

def get_palpites_connection():
    return sqlite3.connect(PALPITES_DB_PATH)

def init_db():
    # Inicializa Banco de Usuários
    conn_u = get_users_connection()
    cursor_u = conn_u.cursor()
    cursor_u.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn_u.commit()
    conn_u.close()
    
    # Inicializa Banco de Palpites
    conn_p = get_palpites_connection()
    cursor_p = conn_p.cursor()
    
    # Tabela de Jogos (necessária para os palpites)
    cursor_p.execute('''
        CREATE TABLE IF NOT EXISTS jogos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time_1 TEXT NOT NULL,
            time_2 TEXT NOT NULL,
            data_hora DATETIME
        )
    ''')
    
    # Tabela de Palpites
    cursor_p.execute('''
        CREATE TABLE IF NOT EXISTS palpites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            jogo_id INTEGER NOT NULL,
            placar_1 INTEGER NOT NULL,
            placar_2 INTEGER NOT NULL,
            FOREIGN KEY (jogo_id) REFERENCES jogos (id)
        )
    ''')
    # Nota: Foreign key para usuarios não pode ser aplicada de forma rígida entre arquivos diferentes sem ATTACH, 
    # mas manteremos a lógica de referência por ID.
    
    conn_p.commit()
    conn_p.close()

def add_user(nome, email, senha):
    conn = get_users_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def email_exists(email):
    """Verifica se um email já está cadastrado."""
    conn = get_users_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM usuarios WHERE email = ?', (email,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def verify_user_login(usuario_login, senha):
    """
    Verifica login. usuario_login pode ser o email ou o 'usuario' (prefixo do email).
    """
    conn = get_users_connection()
    cursor = conn.cursor()
    # Busca por email completo ou por prefixo (antes do @)
    cursor.execute('''
        SELECT id, nome, email FROM usuarios 
        WHERE (email = ? OR substr(email, 1, instr(email, '@') - 1) = ?) 
        AND senha = ?
    ''', (usuario_login, usuario_login, senha))
    user = cursor.fetchone()
    conn.close()
    return user # Retorna (id, nome, email) se encontrado

def add_palpite(usuario_id, jogo_id, placar_1, placar_2):
    conn = get_palpites_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO palpites (usuario_id, jogo_id, placar_1, placar_2)
        VALUES (?, ?, ?, ?)
    ''', (usuario_id, jogo_id, placar_1, placar_2))
    conn.commit()
    palpite_id = cursor.lastrowid
    conn.close()
    return palpite_id

def get_all_users():
    conn = get_users_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    users = cursor.fetchall()
    conn.close()
    return users

def get_all_palpites():
    conn = get_palpites_connection()
    cursor = conn.cursor()
    # Nota: u.nome não está em palpites.db. 
    # Para buscas complexas que unem os dois, precisaríamos de uma lógica que consulte ambos ou use ATTACH. 
    # Por agora, retornamos apenas os dados de palpites.
    cursor.execute('''
        SELECT p.id, p.usuario_id, j.time_1, j.time_2, p.placar_1, p.placar_2
        FROM palpites p
        JOIN jogos j ON p.jogo_id = j.id
    ''')
    palpites = cursor.fetchall()
    conn.close()
    return palpites

if __name__ == "__main__":
    init_db()
    print("Bancos de dados inicializados:")
    print(f"- Usuários: {os.path.abspath(USERS_DB_PATH)}")
    print(f"- Palpites: {os.path.abspath(PALPITES_DB_PATH)}")

