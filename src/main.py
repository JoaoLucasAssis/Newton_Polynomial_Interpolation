import functions.calculo as calc
import functions.interface as gui

def main():
    o =  gui.menu()

    x, y = gui.get_points()
    polynomial = calc.newton_polynomial(x, y)

    if o == 1:
        calc.plot_polynomial(polynomial)
    elif o == 2:
        calc.estimate_velocity(polynomial)
    elif o == 3:
        calc.trapezoidal_rule(x, y)
    elif o == 4:
        target_velocity = 10.00
        result = calc.bisection_method(polynomial, (min(x), max(x)), target_velocity)
        if result is not None:
            print(f"O carro atinge a velocidade de {target_velocity} m/s em t = {result:.5f} segundos.")
    # elif o == 3:
        # calc.plot_polynomial(calc.least_squares(x, y), x, y)
    elif o == 6:
        print("Encerrando o programa...")

if __name__ == "__main__":
    main()