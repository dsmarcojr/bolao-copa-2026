import os
import database

def inicializar():
    """Inicializa o banco de dados."""
    database.init_db()
    print("Bancos de dados inicializados.")

def cadastrar_usuario(nome, email, senha):
    """Cadastra um novo usuário no banco de dados."""
    user_id = database.add_user(nome, email, senha)
    if user_id:
        print(f"Usuário {nome} cadastrado com sucesso! ID: {user_id}")
    else:
        print(f"Erro: O email '{email}' já está em uso.")
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
        print(f"ID: {user[0]} | Nome: {user[1]} | Email: {user[2]}")

def login(usuario_ou_email, senha):
    """Realiza o login do usuário."""
    user = database.verify_user_login(usuario_ou_email, senha)
    if user:
        print(f"Login realizado com sucesso! Bem-vindo, {user[1]}.")
    else:
        print("Erro: Usuário/Email ou senha incorretos.")
    return user

def calcular_pontos(p1, p2, r1, r2):
    """
    Calcula a pontuação de um palpite baseado no resultado real.
    As pontuações são acumulativas, exceto no caso de placar em cheio.
    p1, p2: Gols do mandante e visitante no palpite.
    r1, r2: Gols do mandante e visitante no resultado real.
    """
    # 1. Placar em cheio (10 pontos - soberano)
    if p1 == r1 and p2 == r2:
        return 10
    
    pontos = 0
    # Tendência do palpite e do resultado
    # 1: Mandante, -1: Visitante, 0: Empate
    t_p = 1 if p1 > p2 else (-1 if p1 < p2 else 0)
    t_r = 1 if r1 > r2 else (-1 if r1 < r2 else 0)
    
    # 2. Acerto do vencedor ou empate (+5 pontos)
    if t_p == t_r:
        pontos += 5
        
    # 3. Acerto da quantidade de gols do mandante (+2 pontos)
    if p1 == r1:
        pontos += 2

    # 4. Acerto da quantidade de gols do visitante (+2 pontos)
    if p2 == r2:
        pontos += 2

    # 5. Acerto do placar invertido (+3 pontos)
    # Ex: Palpite 1x2, Resultado 2x1. Não ocorre em empates.
    if p1 == r2 and p2 == r1 and p1 != p2:
        pontos += 3
        
    return pontos

if __name__ == "__main__":
    inicializar()
    # Exemplo de uso via linha de comando
    print("\n--- Sistema de Bolão ---")
    while True:
        print("\n1. Cadastrar Usuário")
        print("2. Listar Usuários")
        print("3. Fazer Login")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            cadastrar_usuario(nome, email, senha)
        elif opcao == "2":
            listar_usuarios()
        elif opcao == "3":
            login_data = input("Usuário ou Email: ")
            senha = input("Senha: ")
            login(login_data, senha)
        elif opcao == "4":
            break
        else:
            print("Opção inválida.")

