import os
import database

def inicializar():
    """Inicializa o banco de dados."""
    database.init_db()
    print("Banco de dados inicializado.")

def cadastrar_usuario(nome, usuario, senha):
    """Cadastra um novo usuário no banco de dados."""
    user_id = database.add_user(nome, usuario, senha)
    if user_id:
        print(f"Usuário {nome} cadastrado com sucesso! ID: {user_id}")
    else:
        print(f"Erro: O usuário '{usuario}' já existe.")
    return user_id

def realizar_palpite(usuario_id, jogo_id, placar_1, placar_2):
    """Registra um palpite para um usuário."""
    palpite_id = database.add_palpite(usuario_id, jogo_id, placar_1, placar_2)
    print(f"Palpite registrado! ID: {palpite_id}")
    return palpite_id

def listar_usuarios():
    """Lista todos os usuários."""
    usuarios = database.get_all_users()
    for user in usuarios:
        print(f"ID: {user[0]} | Nome: {user[1]} | Usuário: {user[2]}")

if __name__ == "__main__":
    inicializar()
    # Exemplo de uso via linha de comando
    print("\n--- Sistema de Bolão ---")
    while True:
        print("\n1. Cadastrar Usuário")
        print("2. Listar Usuários")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            usuario = input("Usuário: ")
            senha = input("Senha: ")
            cadastrar_usuario(nome, usuario, senha)
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            break
        else:
            print("Opção inválida.")
