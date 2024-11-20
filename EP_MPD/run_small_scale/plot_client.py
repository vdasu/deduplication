import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import shutil

# use latex for font rendering with times new roman
# add amsmath package for latex

if shutil.which("latex"):

    plt.rcParams.update(
        {
            "text.usetex": True,
            "font.family": "Times New Roman",
            "font.size": 12,
            "text.latex.preamble": r"\usepackage{amsmath}",
        }
    ) 

# dataset sizes
dsize = [5, 7, 10, 13, 15]
if shutil.which("latex"):
    dsize_labels = ["$2^{5}$", "$2^{7}$", "$2^{10}$", "$2^{13}$", "$2^{15}$"]
else:
    dsize_labels = ["2^5", "2^7", "2^10", "2^13", "2^15"]

# clients size
clients = [5, 10, 15, 20, 25]

# duplication levels
dup_level = [0.1, 0.3, 0.5, 0.7, 0.9]
if shutil.which("latex"):
    dup_labels = ["10\%", "30\%", "50\%", "70\%", "90\%"]
else:
    dup_labels = ["10%", "30%", "50%", "70%", "90%"]


def get_client_times(lines):
    client_times = defaultdict(int)

    for line in lines:
        if "Client" in line:
            if len(line.split(",")) < 2:
                continue
            if "Client" in line.split(",")[1]:
                client_id = int(line.split(",")[0].split(" ")[1])
                client_time = float(line.split(",")[1].split(":")[1].strip())
                client_times[client_id] += client_time

    return client_times


def plot_data(data, data_labels, name):
    # dataset variation plot
    times_t1 = []
    times_t2 = []

    for size in data:
        if name == "dsize":
            path_t1 = f"type1_runs/{size}_10_0.3.log"
            path_t2 = f"type2_runs/{size}_10_0.3.log"
        elif name == "clients":
            path_t1 = f"type1_runs/15_{size}_0.3.log"
            path_t2 = f"type2_runs/15_{size}_0.3.log"
        elif name == "dup":
            path_t1 = f"type1_runs/15_10_{size}.log"
            path_t2 = f"type2_runs/15_10_{size}.log"

        with open(path_t1, "r") as f_t1:
            data_t1 = f_t1.readlines()
        with open(path_t2, "r") as f_t2:
            data_t2 = f_t2.readlines()

        client_times_t1 = get_client_times(data_t1)
        client_times_t2 = get_client_times(data_t2)

        times_t1.append(sum(client_times_t1.values()) / len(client_times_t1))
        times_t2.append(sum(client_times_t2.values()) / len(client_times_t2))

    n = len(data)

    x = np.arange(n)

    width = 0.8

    fig, ax = plt.subplots()

    # Plot bars
    bar1 = ax.bar(
        x - width / 4 - width / 32,
        times_t1,
        width / 2,
        label=r"$\ensuremath{\text {EP-MPD}^{(\text {I})}$" if shutil.which("latex") else "EP-MPD(I)",
    )
    bar2 = ax.bar(
        x + width / 4 + width / 32,
        times_t2,
        width / 2,
        label=r"$\ensuremath{\text {EP-MPD}^{(\text {II})}$" if shutil.which("latex") else "EP-MPD(II)",
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
        ax.set_ylim(min(min(times_t1), min(times_t2)) * 0.5, max(max(times_t1), max(times_t2)) * 1.2)
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(data_labels)
    if name == "dup":
        ax.legend(loc="center left")
    else:
        ax.legend()

    # Labeling the bars
    def autolabel(bars):
        """Attach a text label above each bar in *bars*, displaying its height."""
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{round(height, 2)}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 0.5),  # 3 points vertical offset
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

    autolabel(bar1)
    autolabel(bar2)

    figure_numbers = {
        "dsize": "7b",
        "clients": "6b",
        "dup": "8b"
    }

    # Display the plot
    plt.savefig(f"./Figure_{figure_numbers[name]}.pdf", bbox_inches="tight")


plot_data(dsize, dsize_labels, "dsize")
plot_data(clients, clients, "clients")
plot_data(dup_level, dup_labels, "dup")
