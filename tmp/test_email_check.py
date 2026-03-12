import sys
import os

# Adiciona o diretório src ao path para importar motor e database
sys.path.append(os.path.abspath('src'))

import motor
import database

def test_email_verification():
    # Inicializa o banco (garante que as tabelas existam)
    database.init_db()
    
    test_email = "test@example.com"
    test_name = "Test User"
    test_pass = "123456"
    
    print(f"--- Testando cadastro com email único: {test_email} ---")
    # Tenta cadastrar pela primeira vez
    # Se o email já existir de rodadas anteriores, o motor deve detectar
    if database.email_exists(test_email):
        print(f"O email {test_email} já existe no banco. Removendo para teste limpo...")
        conn = database.get_users_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM usuarios WHERE email = ?', (test_email,))
        conn.commit()
        conn.close()

    user_id1 = motor.cadastrar_usuario(test_name, test_email, test_pass)
    if user_id1:
        print("Primeiro cadastro OK.")
    else:
        print("Erro no primeiro cadastro.")

    print(f"\n--- Testando cadastro duplicado com email: {test_email} ---")
    # Tenta cadastrar novamente com o mesmo email
    user_id2 = motor.cadastrar_usuario("Another User", test_email, "password")
    if user_id2 is None:
        print("Verificação de email duplicado funcionou corretamente!")
    else:
        print(f"ERRO: Permitio cadastro duplicado com ID {user_id2}")

if __name__ == "__main__":
    test_email_verification()
