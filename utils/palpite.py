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
