import argparse

import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser(description='Draw bar plot')
parser.add_argument('infiles',
                    type=str,
                    help='input files')
parser.add_argument("outpath", type=str, help="path of saved figure")
parser.add_argument("--legends", type=str, default=None, help="e.g., man,woman")
parser.add_argument("--xlabels", type=str, default=None, help="e.g., add,mean,max,min")
parser.add_argument("--ylabel", type=str, default=None, help="e.g., count")
#parser.add_argument("--filter", type=str, default="", help="considered values")
#parser.add_argument("--metric", type=str, default="", help="metric of interest, e.g., extrapolate_mape")
#parser.add_argument("--metric-name", type=str, default="", help="the name of the metric of interest, e.g., MAPE")
#parser.add_argument("--cmp-col", type=str, default="pooling", help="the name of the column of interest")
#parser.add_argument("--except-threshold", type=float, default=None, help="remind and filter out exceptional data")
args = parser.parse_args()


def main():
    infiles = args.infiles.strip().split(',')
    legends = args.legends.strip().split(',')
    assert len(infiles) == len(legends), "inconsistent legnth!"
    xlabels = args.xlabels.strip().split(',')

    data = dict()
    for lg, infile in zip(legends, infiles):
        records = list()
        with open(infile, 'r') as ips:
            for line in ips:
                cols = line.strip().split(',')
                records.append([float(v) for v in cols])
        mean = np.mean(np.asarray(records), axis=0)
        std = np.std(np.asarray(records), axis=0)
        data[lg] = (mean, std)
    
    x = np.arange(len(xlabels))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    grp_idx = 0
    for k, v in data.items():
        mean, std = v[0], v[1]
        start = (x - 0.5 * width * len(legends) + 0.5 * width) + grp_idx * width
        rects = ax.bar(start, mean, width, yerr=std, label=k)
        grp_idx += 1
    
    # Add some text for xlabels, title and custom x-axis tick xlabels, etc.
    ax.set_ylabel(args.ylabel)
    #ax.set_title(args.title)
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels)
    ax.legend()

    fig.tight_layout()
    plt.savefig(args.outpath, bbox_inches='tight')
    plt.close()


if __name__=="__main__":
    main()
