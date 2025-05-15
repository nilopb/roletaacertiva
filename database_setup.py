import sqlite3

def criar_banco():
    conn = sqlite3.connect('roleta.db')
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        moedas INTEGER DEFAULT 0,
        is_admin INTEGER DEFAULT 0
    )
    ''')

    # Tabela de palpites (armazenar previsões geradas para histórico)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS palpites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        numeros TEXT,  -- números palpites separados por vírgula
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    ''')

    # Tabela de apostas feitas pelos usuários
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS apostas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        numeros TEXT,  -- números apostados separados por vírgula
        valor INTEGER,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados criado com sucesso.")

if __name__ == '__main__':
    criar_banco()
