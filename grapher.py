import numpy as np
from plotter import plot_graph
from infix_evaluator import evaulate_infix


def main():
    expression = input("f(x) = ").replace(" ", "").lower().replace("exp", "e")
    inputs = np.linspace(-10, 10, 100)
    outputs = [evaulate_infix(expression.replace(
        "x", str(num))) for num in inputs]

    valid_inputs = [inputs[i] for i, y in enumerate(outputs) if y is not None]
    valid_outputs = [y for y in outputs if y is not None]

    plot_graph(valid_inputs, valid_outputs)


if __name__ == "__main__":
    main()
