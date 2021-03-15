# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import argparse

import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='plot')
parser.add_argument('input',
                    type=str,
                    help='file to load data')
parser.add_argument("output", type=str, help="path of saved figure")
parser.add_argument("--has-head", default=False, action='store_true', help="whether hes a head line")
parser.add_argument("--title", type=str, default='', help="title")
parser.add_argument("--rows", type=str, default='', help="row names")
parser.add_argument("--columns", type=str, default='', help="column  names")
parser.add_argument("--cbar-title", type=str, default='', help="title of color bar")
args = parser.parse_args()


def shorten(x1, x2, nb):
    inc = (len(x1)-1) // nb
    new_x1 = list()
    new_x2 = list()
    for i in range(0, len(x1), inc):
        new_x1.append(x1[i])
        new_x2.append(x2[i])
    if len(x1) % inc:
        new_x1.append(x1[-1])
        new_x2.append(x2[-1])
    return new_x1, new_x2


def draw_confusion_matrix(conf_matrix, title, xaxis_title, yaxis_title, cbar_title, save_path):
    fig, ax = plt.subplots(1, 1, figsize=(3.5, 3.5))
    im = ax.imshow(conf_matrix, interpolation='nearest', cmap='YlGn')
    plt.title(title)
    xticks = np.arange(len(xaxis_title))
    yticks = np.arange(len(yaxis_title))
    # shorten the ticks for clutter-free visualization
    if len(xticks) >= 4:
        xticks, xaxis_title = shorten(xticks, xaxis_title, 4)
    if len(yticks) >= 4:
        yticks, yaxis_title = shorten(yticks, yaxis_title, 4)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xticklabels(xaxis_title)
    ax.set_yticklabels(yaxis_title)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    char = ax.figure.colorbar(im, ax=ax)
    char.ax.set_ylabel(cbar_title)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    

def main():
    sims = list()
    cols = args.columns.strip().split(',') if args.columns else None
    with open(args.input, 'r') as ips:
        is_first_line = True
        delimiter = ',' if args.input.endswith("csv") else '\t'
        for line in ips:
            if is_first_line:
                is_first_line = False
                if args.has_head:
                    if len(cols) == 0:
                        cols = line.strip().spit(delimiter)
                    continue
            rc_vals = line.strip().split(delimiter)
            sims.append([float(v) for v in rc_vals])

    rows = args.rows.strip().split(',') if args.rows else None
    if not cols:
        cols = list(range(len(sims[0])))
    if not rows:
        if len(sims) == len(cols):
            rows = cols
        else:
            rows = list(range(len(sims)))

    print(cols)
    print(rows)
    draw_confusion_matrix(sims, args.title, cols, rows, args.cbar_title, args.output)


if __name__=="__main__":
    #print "module test"
    #A = np.array([[0.25, 0.75], [0.8, 0.2]])
    #draw_confusion_matrix(A, 'confusion_matrix', 'x_title', 'y_title', ['a', 'b'], ['x', 'y'], './confusion_matrix0.pdf')
    #B = np.array([[0.9, 0.1], [0, 1]])
    #draw_confusion_matrix(B, 'confusion_matrix', 'x_title', 'y_title', ['a', 'b'], ['x', 'y'], './confusion_matrix1.pdf')
    main()
