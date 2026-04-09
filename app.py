import os
import sqlite3
import re
from datetime import datetime
from pytz import timezone
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from werkzeug.security import generate_password_hash, check_password_hash
from src.db_handler import init_dbs, USUARIOS_DB, SELECOES_DB, PALPITES_DB, PARTIDAS_DB

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)
app.secret_key = 'super_secret_key_bolao'

# Initialize DBs
init_dbs()

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    login_val = data.get('login', '').strip()
    senha = data.get('senha', '')
    
    with get_db_connection(USUARIOS_DB) as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE email = ? OR username = ?",
            (login_val, login_val)
        ).fetchone()
        
    if user and check_password_hash(user['senha'], senha):
        return jsonify({"status": "success", "usuario": user['username'], "nome": user['nome']})
    else:
        return jsonify({"status": "error", "message": "Usuário e/ou senha incorretos ou não existem."}), 401

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    nome = data.get('nome', '').strip()
    email = data.get('email', '').strip()
    senha = data.get('senha', '')
    username = email.split('@')[0] if '@' in email else email

    if not '@' in email:
        return jsonify({"status": "error", "message": "Email inválido"}), 400

    hashed_senha = generate_password_hash(senha)
    try:
        with get_db_connection(USUARIOS_DB) as conn:
            conn.execute(
                "INSERT INTO users (nome, username, email, senha) VALUES (?, ?, ?, ?)",
                (nome, username, email, hashed_senha)
            )
        return jsonify({"status": "success", "usuario": username})
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "O Email já está em uso!"}), 400

def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def auto_update_results():
    """Background task to simulate checking/updating results"""
    print(f"[{datetime.now()}] Verifying updates for matches...")
    # Em um cenário real, chamaria uma API esportiva e atualizaria o PARTIDAS_DB
    pass

scheduler = BackgroundScheduler()
scheduler.add_job(auto_update_results, 'interval', seconds=120)
scheduler.start()

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome', '')
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        senha = request.form.get('senha', '')

        # Validations
        if len(nome) < 3 or len(username) < 3:
            flash("Nome e Username devem ter pelo menos 3 caracteres.", "error")
            return render_template('cadastro.html')
        
        if "@" not in email or "." not in email:
            flash("Email inválido.", "error")
            return render_template('cadastro.html')
            
        if len(senha) < 8 or not re.search(r'[A-Z]', senha) or not re.search(r'[a-z]', senha) or not re.search(r'\d', senha):
            flash("A senha deve ter no mínimo 8 caracteres, 1 maiúscula, 1 minúscula e 1 número.", "error")
            return render_template('cadastro.html')

        try:
            hashed_senha = generate_password_hash(senha)
            with get_db_connection(USUARIOS_DB) as conn:
                conn.execute(
                    "INSERT INTO users (nome, username, email, senha) VALUES (?, ?, ?, ?)",
                    (nome, username, email, hashed_senha)
                )
            flash("Cadastro realizado com sucesso! Faça login.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username ou Email já existem.", "error")
            return render_template('cadastro.html')

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_val = request.form.get('login', '')
        senha = request.form.get('senha', '')
        
        with get_db_connection(USUARIOS_DB) as conn:
            user = conn.execute(
                "SELECT * FROM users WHERE email = ? OR username = ?",
                (login_val, login_val)
            ).fetchone()
            
        if user and check_password_hash(user['senha'], senha):
            session['user_id'] = user['id']
            session['is_admin'] = user['is_admin']
            session['nome'] = user['nome']
            return redirect(url_for('home'))
        else:
            flash("Credenciais inválidas.", "error")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    tz = timezone('America/Sao_Paulo')
    now = datetime.now(tz)
    current_date = now.strftime('%Y-%m-%d')
    current_hour = now.hour
    
    can_bet_today = 4 <= current_hour < 12

    if request.method == 'POST':
        # Processing bets
        match_id = int(request.form.get('match_id'))
        score_home = int(request.form.get('score_home'))
        score_away = int(request.form.get('score_away'))
        
        with get_db_connection(PARTIDAS_DB) as conn_partidas:
            match = conn_partidas.execute("SELECT * FROM matches WHERE id = ?", (match_id,)).fetchone()
            
        if match:
            # Check time constraints
            if match['data_jogo'] == current_date and not can_bet_today:
                flash("Fora do horário permitido para jogos de hoje (04:00 - 12:00 allowed).", "error")
            elif match['data_jogo'] < current_date:
                flash("Não é possível palpitar em jogos passados.", "error")
            else:
                try:
                    with get_db_connection(PALPITES_DB) as conn_palpites:
                        conn_palpites.execute(
                            '''INSERT INTO bets (user_id, match_id, home_team_id, away_team_id, score_home, score_away) 
                               VALUES (?, ?, ?, ?, ?, ?)
                               ON CONFLICT(user_id, match_id) DO UPDATE SET score_home=excluded.score_home, score_away=excluded.score_away''',
                            (session['user_id'], match_id, match['home_team_id'], match['away_team_id'], score_home, score_away)
                        )
                    flash("Palpite salvo!", "success")
                except Exception as e:
                    flash(f"Erro ao salvar palpite: {e}", "error")
                    
        return redirect(url_for('home'))

    # Fetch matches
    with get_db_connection(PARTIDAS_DB) as conn_partidas:
        if can_bet_today:
            matches_query = "SELECT * FROM matches WHERE data_jogo >= ? ORDER BY data_jogo, horario_jogo"
            matches = conn_partidas.execute(matches_query, (current_date,)).fetchall()
        else:
            # Only future dates
            matches_query = "SELECT * FROM matches WHERE data_jogo > ? ORDER BY data_jogo, horario_jogo"
            matches = conn_partidas.execute(matches_query, (current_date,)).fetchall()

    # Load teams
    with get_db_connection(SELECOES_DB) as conn_selecoes:
        teams = {row['id']: row['nome_selecao'] for row in conn_selecoes.execute("SELECT * FROM teams").fetchall()}

    # Load user bets
    with get_db_connection(PALPITES_DB) as conn_palpites:
        bets_raw = conn_palpites.execute("SELECT * FROM bets WHERE user_id = ?", (session['user_id'],)).fetchall()
        user_bets = {bet['match_id']: bet for bet in bets_raw}

    display_matches = []
    for m in matches:
        m_dict = dict(m)
        m_dict['home_team_name'] = teams.get(m['home_team_id'], "Unknown")
        m_dict['away_team_name'] = teams.get(m['away_team_id'], "Unknown")
        # Check if already bet
        bet = user_bets.get(m['id'])
        if bet:
            m_dict['bet_home'] = bet['score_home']
            m_dict['bet_away'] = bet['score_away']
        else:
            m_dict['bet_home'] = ''
            m_dict['bet_away'] = ''
        display_matches.append(m_dict)

    return render_template('index.html', matches=display_matches, date=current_date, time=now.strftime("%H:%M:%S"), can_bet_today=can_bet_today)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if not session.get('is_admin'):
        flash("Acesso não autorizado.", "error")
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        match_id = int(request.form.get('match_id'))
        score_home = int(request.form.get('score_home'))
        score_away = int(request.form.get('score_away'))
        
        with get_db_connection(PARTIDAS_DB) as conn:
            conn.execute(
                "UPDATE matches SET resultado_home = ?, resultado_away = ? WHERE id = ?",
                (score_home, score_away, match_id)
            )
        flash("Resultado oficial atualizado com sucesso!", "success")
        return redirect(url_for('admin'))
        
    with get_db_connection(PARTIDAS_DB) as conn_partidas:
        matches = conn_partidas.execute("SELECT * FROM matches ORDER BY data_jogo DESC, horario_jogo DESC").fetchall()
        
    with get_db_connection(SELECOES_DB) as conn_selecoes:
        teams = {row['id']: row['nome_selecao'] for row in conn_selecoes.execute("SELECT * FROM teams").fetchall()}
        
    display_matches = []
    for m in matches:
        m_dict = dict(m)
        m_dict['home_team_name'] = teams.get(m['home_team_id'], "Unknown")
        m_dict['away_team_name'] = teams.get(m['away_team_id'], "Unknown")
        display_matches.append(m_dict)
        
    return render_template('admin.html', matches=display_matches)

@app.route('/resultados')
def resultados():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    with get_db_connection(PARTIDAS_DB) as conn_partidas:
        matches = conn_partidas.execute("SELECT * FROM matches WHERE resultado_home IS NOT NULL ORDER BY data_jogo DESC").fetchall()
        
    with get_db_connection(SELECOES_DB) as conn_selecoes:
        teams = {row['id']: row['nome_selecao'] for row in conn_selecoes.execute("SELECT * FROM teams").fetchall()}

    display_matches = []
    for m in matches:
        m_dict = dict(m)
        m_dict['home_team_name'] = teams.get(m['home_team_id'], "Unknown")
        m_dict['away_team_name'] = teams.get(m['away_team_id'], "Unknown")
        display_matches.append(m_dict)

    return render_template('resultados.html', matches=display_matches)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
