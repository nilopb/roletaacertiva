from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from utils.palpite import gerar_palpites  # depois vou enviar essa função
from functools import wraps

app = Flask(__name__)
app.secret_key = 'sua_chave_super_secreta'

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Decorator para exigir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rota: Página Inicial / Home (Área do Usuário)
@app.route('/')
@login_required
def home():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT username, moedas FROM users WHERE id = ?", (session['user_id'],))
    user = cur.fetchone()
    palpites = gerar_palpites()  # aqui usamos a função de IA/matemática para palpites exatos
    conn.close()
    return render_template('home.html', username=user['username'], moedas=user['moedas'], palpites=palpites)

# Rota: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()
        conn.close()
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha incorretos.')
    return render_template('login.html')

# Rota: Cadastro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        cur = conn.cursor()
        # Verifica se usuário já existe
        cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cur.fetchone():
            flash('Usuário já existe.')
            conn.close()
            return redirect(url_for('register'))
        # Insere usuário novo
        cur.execute("INSERT INTO users (username, password, moedas) VALUES (?, ?, ?)", (username, password, 50))
        conn.commit()
        conn.close()
        flash('Cadastro realizado com sucesso! Faça login.')
        return redirect(url_for('login'))
    return render_template('register.html')

# Rota: Logout
@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

# Rota: Admin (painel)
@app.route('/admin')
@login_required
def admin():
    # Apenas usuário admin com username 'admin' pode acessar
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE id = ?", (session['user_id'],))
    user = cur.fetchone()
    if user['username'] != 'admin':
        flash('Acesso negado.')
        return redirect(url_for('home'))
    
    cur.execute("SELECT id, username, moedas FROM users")
    users = cur.fetchall()
    conn.close()
    return render_template('admin.html', users=users)

# Mais rotas como simulador, roleta, etc, virão depois.

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/simulador', methods=['GET', 'POST'])
@login_required
def simulador():
    resultado = None
    if request.method == 'POST':
        numero = int(request.form['numero'])
        valor = float(request.form['valor'])
        # Simulação básica: ganha se o número for igual ao sorteado (aleatório)
        import random
        sorteado = random.randint(0, 36)
        if numero == sorteado:
            resultado = f'Você ganhou! Número sorteado: {sorteado}. Ganho: R${valor * 35:.2f}'
        else:
            resultado = f'Você perdeu. Número sorteado: {sorteado}. Perda: R${valor:.2f}'
    return render_template('simulador.html', resultado=resultado)
