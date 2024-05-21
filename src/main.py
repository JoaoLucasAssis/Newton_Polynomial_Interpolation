import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

def get_time_input():
    """
    Solicita e valida a entrada do usuário para o tempo desejado.

    Returns:
        int: O tempo inserido pelo usuário.
    """

    print("\x1b[2J\x1b[1;1H") # Limpa a tela do terminal

    while True:
        try:
            n = int(input("Qual tempo você gostaria de saber a velocidade? (Digite -1 para sair): "))
            if n >= -1:
                return n
            else:
                print("Entrada inválida. Por favor, insira um número maior ou igual a -1.")
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro.")

def estimate_velocity(polynomial):
    """
    Estima a velocidade do carro nos tempos não medidos usando o polinômio de interpolação.

    Args:
        polynomial (sp.Expr): O polinômio de interpolação de Newton
    """

    print("\x1b[2J\x1b[1;1H") # Limpa a tela do terminal

    n = get_time_input()

    while n != -1:
        print("\x1b[2J\x1b[1;1H") # Limpa a tela do terminal

        velocity = float(polynomial.subs('x', n))
        print(f"Velocidade do carro no tempo {n}s: {velocity} m/s.")

        n = get_time_input()

def plot_polynomial(polynomial):
    lamba = eval(f"lambda x: {polynomial}")

    x = np.linspace(-10, 10, 100)
    y = lamba(x)

    plt.plot(x, y, 'r', linewidth=1)
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)

    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.title(f'P(x): {polynomial}')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

def newton_polynomial(x, y):
    """
    Constrói o polinômio de interpolação de Newton para os pontos fornecidos (x, y) utilizando as diferenças divididas.

    Args:
        x (list): Lista dos pontos x
        y (list): Lista dos pontos y

    Execução:
    1.0 - Calcula os coeficientes das diferenças divididas
    2.0 - Inicializa o polinômio com o primeiro coeficiente
    3.0 - Define o símbolo x para construir o polinômio
    4.0 - Para cada próximo coeficiente:
        4.1 - Cria uma variável temporária(term) que recebe o coeficiente
        4.2 - Multiplica o coeficiente pela expressão (x - x[j]) j vezes, onde j é o índice do coeficiente
        4.3 - Soma o termo ao polinômio
    5.0 - Retorna a expressão expandida do polinômio de interpolação de Newton

    Returns:
        sp.Expr: O polinômio de interpolação de Newton como uma expressão totalmente expandida
    """
    
    coef = divided_differences(x, y) # 1.0
    n = len(coef)

    polynomial = coef[0] # 2.0

    x_symbol = sp.symbols('x') # 3.0

    # 4.0
    for i in range(1, n):
        term = coef[i] # 4.1

        for j in range(i): 
            term *= (x_symbol - x[j]) # 4.2

        polynomial += term # 4.3

    return sp.expand(polynomial) # 5.0

def divided_differences(x, y):
    """
    Executa o cálculo das diferenças divididas de Newton para os pontos fornecidos (x, y)

    Args:
        x (list): Lista dos pontos x
        y (list): Lista dos pontos y

    Execução:
    1.0 - Inicializa a tabela de diferenças divididas com zeros
        1.1 - Preenche a primeira coluna da tabela com os valores de y
    2.0 - Para cada ordem de diferença:
        2.1 - Calcula a diferença de primeira ordem
        2.2 - Calcula a diferença de ordem superior
    3.0 Retorna a diagonal da tabela, contendo os coeficientes

    Returns:
        np.diag(table): Os coeficientes presentes na diagonal da tabela de diferenças divididas
    """

    n = len(y)
    table = np.zeros((n, n)) # 1.0

    table[:, 0] = y # 1.1

    # 2.0
    for j in range(1, n):  # Loop para cada coluna
        for i in range(j, n):  # Loop para cada linha
            if j == 1:
                table[i, j] = (table[i, 0] - table[i - 1, 0]) / (x[i] - x[i - 1]) # 2.1
            else:
                table[i, j] = (table[i, j - 1] - table[i - 1, j - 1]) / (x[i] - x[i - j]) # 2.2

    return np.diag(table) # 3.0

def get_points():
    """
    Solicita ao usuário a inserção de um número de pontos, depois coleta e retorna esses pontos.

    Execução:
    1.0 - Pergunta ao usuário quantos pontos ele deseja inserir
        1.1 - Valida a entrada para garantir que é um número inteiro positivo
    2.0 - Para cada ponto:
        2.1 - Solicita ao usuário que insira o valor de x
        2.2 - Solicita ao usuário que insira o valor de y
        2.3 - Converte e armazena os valores de entrada como floats
    3.0 - Retorna dois arrays com os valores de x e y coletados

    Returns:
        (x, y) - Tupla contendo os arrays dos pontos x e y
    """

    print("\x1b[2J\x1b[1;1H") # Limpa a tela do terminal

    n = int(input("Quantos pontos deseja inserir? "))  # 1.0

    # 1.1
    while n <= 0:  
        print("\x1b[2J\x1b[1;1H") # Limpa a tela do terminal
        print(f"Entrada inválida: {n}. Por favor, insira um número inteiro positivo.")
        n = int(input("Quantos pontos deseja inserir? "))

    x = [] 
    y = []

    # 2.0
    for i in range(n):  
        x_input = input(f"Digite o valor de x para o ponto {i+1}: ").strip() # 2.1
        y_input = input(f"Digite o valor de y para o ponto {i+1}: ").strip() # 2.2

        x.append(float(x_input)) # 2.3
        y.append(float(y_input)) # 2.3

        print("\x1b[2J\x1b[1;1H") # Limpa a tela do terminal

    return np.array(x), np.array(y)  # 3.0

def main():
    x, y = get_points()
    polynomial = newton_polynomial(x, y)

if __name__ == "__main__":
    main()