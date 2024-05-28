import functions.calculo as calc
import functions.interface as gui
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

def least_squares(x, y):
    n = len(x)
    
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_squared = sum(x_data ** 2 for x_data in x)
    sum_x_times_y = sum(x_data * y_data for x_data, y_data in zip(x, y))

    mean_x = sum_x / n
    mean_y = sum_y / n

    b = ((n * sum_x_times_y) - (sum_x * sum_y)) / ((n * sum_x_squared) - (sum_x ** 2))
    a = mean_y - b * mean_x

    x_symbol = sp.symbols('x')
    polynomial = b * x_symbol + a

    return sp.expand(polynomial)

def get_time_input():
    """
    Solicita e valida a entrada do usuário para o tempo desejado.

    Returns:
        int: O tempo inserido pelo usuário.
    """

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

def plot_polynomial(polynomial, x, y):
    lamba = eval(f"lambda x: {polynomial}")

    x_vals = np.linspace(-10, 10, 100)
    y_vals = lamba(x_vals)

    plt.plot(x_vals, y_vals, 'r', linewidth=1)
    plt.scatter(x, y, color='red', label='Data points')
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

def menu():
    """
    Exibe um menu com opções para mostrar um gráfico ou gerar velocidades para tempos não medidos.
    """

    print("\x1b[2J\x1b[1;1H") # Limpa a tela do terminal

    print("Menu")
    print("1. Mostrar gráfico\n2. Mostrar velocidades\n3. Mínimos quadrados\n4. Sair")

    o = int(input("Escolha uma opção: ").strip())

    while o not in [1, 2, 3, 4]:
        print("\x1b[2J\x1b[1;1H") # Limpa a tela do terminal

        print("Opção inválida. Digite uma das opções abaixo.")
        print("1. Mostrar gráfico\n2. Mostrar velocidades\n3. Mínimos quadrados\n4. Sair")
        o = int(input("Escolha uma opção: ").strip())
    
    return o

def main():
    o =  gui.menu()

    x, y = gui.get_points()
    polynomial = calc.newton_polynomial(x, y)

    if o == 1:
        calc.plot_polynomial(polynomial)
    elif o == 2:
        calc.estimate_velocity(polynomial)
    elif o == 3:
        plot_polynomial(least_squares(x, y), x, y)
    elif o == 4:
        print("Encerrando o programa...")

if __name__ == "__main__":
    main()