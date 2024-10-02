import matplotlib.pyplot as plt
import numpy as np

# use latex for font rendering with times new roman
# add amsmath package for latex
plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "Times New Roman",
        "font.size": 12,
        "text.latex.preamble": r"\usepackage{amsmath}",
    }
)

# dataset sizes
dsize = [10, 11, 13, 15, 17, 19]
dsize_labels = ["$2^{10}$", "$2^{11}$", "$2^{13}$", "$2^{15}$", "$2^{17}$", "$2^{19}$"]

# clients size
clients = [10, 20, 30, 40, 50]

# duplication levels
dup_level = [0.1, 0.3, 0.5, 0.7, 0.9]
dup_labels = ["10\%", "30\%", "50\%", "70\%", "90\%"]


def plot_data(data, data_labels, name):
    # dataset variation plot
    times_t1 = []
    times_t2 = []

    for size in data:
        if name == "dsize":
            path_t1 = f"type1_runs/{size}_50_0.3.log"
            path_t2 = f"type2_runs/{size}_50_0.3.log"
        elif name == "clients":
            path_t1 = f"type1_runs/19_{size}_0.3.log"
            path_t2 = f"type2_runs/19_{size}_0.3.log"
        elif name == "dup":
            path_t1 = f"type1_runs/19_50_{size}.log"
            path_t2 = f"type2_runs/19_50_{size}.log"

        with open(path_t1, "r") as f_t1:
            data_t1 = f_t1.readlines()
        with open(path_t2, "r") as f_t2:
            data_t2 = f_t2.readlines()

        for line in data_t1[::-1]:
            if "Total time for entire protocol" in line:
                times_t1.append(float(line.split(":")[1]))
                break

        for line in data_t2[::-1]:
            if "Total time for entire protocol" in line:
                times_t2.append(float(line.split(":")[1]))
                break

    n = len(data)

    x = np.arange(n)

    width = 0.8

    fig, ax = plt.subplots()

    # Plot bars
    bar1 = ax.bar(
        x - width / 4 - width / 32,
        times_t1,
        width / 2,
        label=r"$\ensuremath{\text {EP-MPD}^{(\text {I})}$",
    )
    bar2 = ax.bar(
        x + width / 4 + width / 32,
        times_t2,
        width / 2,
        label=r"$\ensuremath{\text {EP-MPD}^{(\text {II})}$",
    )

    # Add some text for labels, title, and custom x-axis tick labels, etc.
    if name == "dsize":
        ax.set_xlabel("Dataset Size")
    elif name == "clients":
        ax.set_xlabel("Number of Clients")
    elif name == "dup":
        ax.set_xlabel("Duplication Percentage")
    ax.set_ylabel("Time (secs)")

    # set y limit as 8000
    if name == "dsize":
        ax.set_ylim(min(min(times_t1), min(times_t2)) * 0.5, max(max(times_t1), max(times_t2)) * 2.0)
    elif name == "dup":
        ax.set_ylim(min(min(times_t1), min(times_t2)) * 0.5, max(max(times_t1), max(times_t2)) * 1.2)
    elif name == "clients":
        ax.set_ylim(min(min(times_t1), min(times_t2)) * 0.5, max(max(times_t1), max(times_t2)) * 1.5)
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(data_labels)
    if name == "dup":
        ax.legend(loc="center left")
    else:
        ax.legend()

    # Labeling the bars
    def autolabel(bars):
        neg_off = 2
        """Attach a text label above each bar in *bars*, displaying its height."""
        for bar in bars:
            height = bar.get_height()
            if name == "dsize":
                ax.annotate(
                    f"{round(height, 1)}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0 - neg_off, 0.5),  # 3 points vertical offset
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                )
            else:
                ax.annotate(
                    f"{round(height, 1)}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 0.5),  # 3 points vertical offset
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                )

    autolabel(bar1)
    autolabel(bar2)

    figure_numbers = {
        "dsize": "7a",
        "clients": "6a",
        "dup": "8a"
    }

    # Display the plot
    plt.savefig(f"./Figure_{figure_numbers[name]}.pdf", bbox_inches="tight")


plot_data(dsize, dsize_labels, "dsize")
plot_data(clients, clients, "clients")
plot_data(dup_level, dup_labels, "dup")