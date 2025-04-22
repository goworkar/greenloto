# by Arthur Beowulf - Developed System
#2022

import itertools
import sqlite3


# Função para verificar se a linha tem 10 números consecutivos
def has_consecutive(numbers):
    # Ordenar os números (embora o itertools.combinations já ordene as combinações)
    numbers = sorted(numbers)

    # Inicializa o contador de números consecutivos
    consecutive_count = 1  # Começa com 1 porque o primeiro número já é contado
    max_consecutive = 10  # Número mínimo de números consecutivos que tornam a linha inválida

    # Verificar sequências consecutivas
    for i in range(1, len(numbers)):
        if numbers[i] == numbers[i - 1] + 1:  # Se o número atual for consecutivo ao anterior
            consecutive_count += 1
        else:
            # Se a sequência for interrompida, reinicia o contador
            consecutive_count = 1

        # Se encontrar 10 ou mais números consecutivos, a linha é inválida
        if consecutive_count >= max_consecutive:
            return True

    # Se nenhuma sequência de 10 ou mais números consecutivos for encontrada, retorna False
    return False

# Função para verificar se a linha tem exatamente 13 números ímpares
def has_thirteen_odds(numbers):
    odd_count = sum(1 for num in numbers if num % 2 != 0)
    return odd_count == 13


# Função para verificar se a linha tem exatamente 12 números pares
def has_twelve_evens(numbers):
    even_count = sum(1 for num in numbers if num % 2 == 0)
    return even_count == 12


# Função para verificar a sequência com três números saltando dois
def has_intersectlist1(numbers):
    lista = [1, 2, 3, 6, 7, 8, 11, 12, 13, 16, 17, 18, 21, 22, 23]
    intersecao = list(set(lista) & set(numbers))
    return  len(intersecao) == 15

def has_intersectlist2(numbers):
    lista = [2, 3, 4, 7, 8, 9, 12, 13, 14, 17, 18, 19, 22, 23, 24]
    intersecao = list(set(lista) & set(numbers))
    return  len(intersecao) == 15

def has_intersectlist3(numbers):
    lista = [3, 4, 5, 8, 9, 10, 13, 14, 15, 18, 19, 20, 23, 24, 25]
    intersecao = list(set(lista) & set(numbers))
    return  len(intersecao) == 15


# Função para verificar todas as regras
def is_valid_line(numbers):
    # Ordena os números para garantir que a ordem crescente seja respeitada
    numbers = sorted(numbers)

    retornopadrao = False;
    # Aplicando todas as restrições
    if not(has_consecutive(numbers)):
        if not(has_thirteen_odds(numbers)):
            if not(has_twelve_evens(numbers)):
                if not(has_intersectlist1(numbers)):
                    if not (has_intersectlist2(numbers)):
                        if not (has_intersectlist3(numbers)):
                            retornopadrao = True
    return retornopadrao


# Passo 1: Gerar as combinações de 15 números entre 1 e 25
combinations = itertools.combinations(range(1, 26), 15)

# Passo 2: Estabelecer a conexão com o banco de dados SQLite
conn = sqlite3.connect('lottery.db')
cursor = conn.cursor()

# Passo 3: Criar a tabela (se não existir)
cursor.execute('''
CREATE TABLE IF NOT EXISTS lottery_combinations (
    id integer PRIMARY KEY AUTOINCREMENT,
    numbers TEXT
)
''')

# Passo 4: Inserir as combinações no banco de dados, com as validações
valid_count = 0
for combination in combinations:

    if is_valid_line(combination):
        # Transformando a tupla de números em uma string separada por vírgulas
        combination_str = ','.join(map(str, combination))
        cursor.execute('INSERT INTO lottery_combinations (numbers) VALUES (?)', (combination_str,))
        valid_count += 1
        combination_str = ''

# Commitar as mudanças e fechar a conexão
conn.commit()
conn.close()

print(f"Total de linhas válidas inseridas: {valid_count}")
