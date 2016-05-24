# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

def draw_confusion_matrix(conf_matrix, title, xaxis_title, yaxis_title, xaxis_labels, yaxis_labels, save_path):
    plt.figure()
    plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.gray)
    plt.title(title)
    plt.colorbar()
    plt.xticks(range(len(xaxis_labels)), xaxis_labels[:len(xaxis_labels)], rotation=-45)
    plt.yticks(range(len(yaxis_labels)), yaxis_labels[:len(yaxis_labels)])
    plt.xlabel(xaxis_title)
    plt.ylabel(yaxis_title)
    plt.tight_layout()
    plt.savefig(save_path, format=save_path[1+save_path.rfind('.'):])
    
if __name__=="__main__":
    print "module test"
    A = np.array([[0.25, 0.75], [0.8, 0.2]])
    draw_confusion_matrix(A, 'confusion_matrix', 'x_title', 'y_title', ['a', 'b'], ['x', 'y'], './confusion_matrix0.pdf')
    B = np.array([[0.9, 0.1], [0, 1]])
    draw_confusion_matrix(B, 'confusion_matrix', 'x_title', 'y_title', ['a', 'b'], ['x', 'y'], './confusion_matrix1.pdf')