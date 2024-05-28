import numpy as np

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
            
def menu():
    """
    Exibe um menu com opções para mostrar um gráfico ou gerar velocidades para tempos não medidos.
    """

    print("\x1b[2J\x1b[1;1H") # Limpa a tela do terminal

    print("Menu")
    print("1. Mostrar gráfico\n2. Mostrar velocidades\n3. Sair")

    o = int(input("Escolha uma opção: ").strip())

    while o not in [1, 2, 3]:
        print("\x1b[2J\x1b[1;1H") # Limpa a tela do terminal

        print("Opção inválida. Digite uma das opções abaixo.")
        print("1. Mostrar gráfico\n2. Mostrar velocidades\n3. Sair")
        o = int(input("Escolha uma opção: ").strip())
    
    return o