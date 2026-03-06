import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data.json')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"apostas": [], "jogos": [], "usuarios": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    print("Motor do bolão iniciado.")
    dados = load_data()
    print(f"Banco de dados carregado com {len(dados.get('usuarios', []))} usuários.")
