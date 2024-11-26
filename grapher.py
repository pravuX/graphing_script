import numpy as np
from plotter import plot_graph
from infix_evaluator import evaulate_infix


def prompt():
    expression = input("f(x) = ")
    expression = expression.replace(" ", "").lower().replace("exp", "e")
    return expression


def main():
    print("Enter an expression(Ctrl+C to exit).")
    try:
        while True:
            expression = prompt()
            inputs = np.linspace(-100, 100, 100)
            outputs = [evaulate_infix(expression,num) for num in inputs]

            valid_inputs = [inputs[i]
                            for i, y in enumerate(outputs) if y is not None]
            valid_outputs = [y for y in outputs if y is not None]

            plot_graph(valid_inputs, valid_outputs)
    except KeyboardInterrupt:
        print("\nProgram exited by user.")


if __name__ == "__main__":
    main()
