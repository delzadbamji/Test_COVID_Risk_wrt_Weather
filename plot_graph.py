import pandas as pd
import matplotlib.pyplot as plt


def plot_cluster(X, Y, labels):
    data = pd.DataFrame({"X": X, "Y": Y, "Class": labels})
    groups = data.groupby("Class")
    for name, group in groups:
        plt.plot(group["X"], group["Y"], marker="o", linestyle="", label=name)
    plt.legend()
    plt.show()


def test_plot_cluster():
    X = [6,8,7,6,5,7,5,9,10,4]
    Y = [8,6,6,10,1,1,1,9,8,9]
    labels = [3,1,2,2,3,1,2,2,2,1]
    plot_cluster(X, Y, labels)

if __name__ == '__main__':
    test_plot_cluster()