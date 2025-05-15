import numpy as np
from collections import Counter

# Simula coleta dos últimos 100 números da roleta (exemplo real: coletar do site, mas aqui hardcoded)
def coletar_ultimos_numeros():
    # Números entre 0 e 36, simulando resultados
    # Aqui você pode trocar para puxar do site real via scraping ou API depois
    np.random.seed(42)  # fixar seed para exemplo consistente
    return list(np.random.randint(0, 37, size=100))

# Função para gerar 5 palpites matemáticos (números mais frequentes + tendência)
def gerar_palpites():
    ultimos_numeros = coletar_ultimos_numeros()

    # Contagem de frequência dos números
    freq = Counter(ultimos_numeros)
    
    # Os 5 números mais frequentes nos últimos 100 resultados
    mais_frequentes = [num for num, count in freq.most_common(5)]

    return mais_frequentes
import sqlite3
from collections import Counter

DATABASE = 'database.db'

def gerar_palpites():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    # Supondo que você tenha uma tabela 'resultados' com coluna 'numero' para últimos resultados da roleta
    cur.execute("SELECT numero FROM resultados ORDER BY id DESC LIMIT 100")
    resultados = [row[0] for row in cur.fetchall()]
    conn.close()

    if not resultados:
        # Se não tiver resultados, retorna palpites fixos (exemplo)
        return [0, 1, 2, 3, 4]

    # Contar frequências dos números
    contagem = Counter(resultados)
    # Pegar os 5 números mais frequentes
    mais_comuns = [num for num, freq in contagem.most_common(5)]
    return mais_comuns
