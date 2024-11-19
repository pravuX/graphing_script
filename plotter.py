import matplotlib.pyplot as plt


def plot_graph(inputs, outputs):
    fig, ax = plt.subplots()
    ax.plot(inputs, outputs, label="f(x)", color="red")
    ax.grid(True, which='both')

    # set the x and y spines at orign
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    # turn off the top and right ticks/spines
    ax.spines['top'].set_color('none')
    ax.xaxis.tick_bottom()
    ax.spines['right'].set_color('none')
    ax.yaxis.tick_left()

    ax.set_xlabel("x", loc="right")
    ax.set_ylabel("f(x)", loc="top")
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)

    plt.show()
