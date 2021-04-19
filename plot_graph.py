import pandas as pd
import matplotlib.pyplot as plt


def plot_cluster(X, Y, labels, probabilities):
    color_list = ['#FF2D00', '#FF7100', '#FFA900', '#FFCE00', '#FFEC00', '#E9FF00', '#ADFF00', '#80FF00', '#00FF8B', '#00E1FF']
    color_label = ['0.0-0.1 (Low Risk)', '0.1-0.2', '0.2-0.3', '0.3-0.4', '0.4-0.5', '0.5-0.6', '0.6-0.7', '0.7-0.8', '0.8-0.9', '0.9-1.0 (High Risk)']

    colors = []
    new_labels = []
    for p in probabilities:
        if p<0.1:
            colors.append(color_list[0])
            new_labels.append(color_label[0])
        elif p<0.2:
            colors.append(color_list[1])
            new_labels.append(color_label[1])
        elif p<0.3:
            colors.append(color_list[2])
            new_labels.append(color_label[2])
        elif p<0.4:
            colors.append(color_list[3])
            new_labels.append(color_label[3])
        elif p<0.5:
            colors.append(color_list[4])
            new_labels.append(color_label[4])
        elif p<0.6:
            colors.append(color_list[5])
            new_labels.append(color_label[5])
        elif p<0.7:
            colors.append(color_list[6])
            new_labels.append(color_label[6])
        elif p<0.8:
            colors.append(color_list[7])
            new_labels.append(color_label[7])
        elif p<0.9:
            colors.append(color_list[8])
            new_labels.append(color_label[8])
        elif p<=1.0:
            colors.append(color_list[9])
            new_labels.append(color_label[9])

    data = pd.DataFrame({"X": X, "Y": Y, "Class": new_labels, "Colors": colors})

    groups = data.groupby("Class")

    for name, group in groups:
        plt.plot(group["X"], group["Y"], marker="o", linestyle="", label=name, markersize=3)
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.title('Risk Probabilities of Regions')
    plt.legend()
    plt.show()
