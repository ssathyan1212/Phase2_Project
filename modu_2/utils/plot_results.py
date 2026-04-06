import matplotlib.pyplot as plt
import numpy as np

def plot_metrics(acc, prec, rec, f1):
    labels = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    values = [acc, prec, rec, f1]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Evaluation Metrics")
    plt.ylabel("Score")
    plt.ylim(0, 1)

    for i, v in enumerate(values):
        plt.text(i, v + 0.02, str(round(v, 2)), ha='center')

    plt.savefig("output/metrics_bar.png")
    plt.show()


def plot_confusion_matrix(cm):
    plt.figure()
    plt.imshow(cm)

    plt.title("Confusion Matrix")
    plt.colorbar()

    labels = ['Positive', 'Negative']
    plt.xticks([0,1], labels)
    plt.yticks([0,1], labels)

    for i in range(2):
        for j in range(2):
            plt.text(j, i, cm[i][j], ha='center', va='center')

    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.savefig("output/confusion_matrix.png")
    plt.show()


def plot_accuracy_trend(history):
    plt.figure()
    plt.plot(history, marker='o')

    plt.title("Accuracy over Time")
    plt.xlabel("Step")
    plt.ylabel("Accuracy")

    plt.savefig("output/accuracy_trend.png")
    plt.show()