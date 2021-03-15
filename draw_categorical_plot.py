from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='plot')
parser.add_argument('inputs',
                    type=str,
                    help='folder to load data')
parser.add_argument("output", type=str, help="path of saved figure")
parser.add_argument("--has-head", default=False, action='store_true', help="whether hes a head line")
parser.add_argument("--legends", type=str, default=None, help="legend infomation")
parser.add_argument("--cate-idx", type=int, default=0, help="column of category")
parser.add_argument("--value-idx", type=int, default=1, help="column of value")
parser.add_argument("--std-idx", type=int, default=-1, help="column of std")
args = parser.parse_args()


def load_data(legends, files):
    all_data = dict()
    for k, f in zip(legends, files):
        data = dict()
        with open(f, 'r') as ips:
            is_first_line = True
            delimiter = ',' if f.endswith("csv") else '\t'
            for line in ips:
                if is_first_line:
                    is_first_line = False
                    if args.has_head:
                        continue
                cols = line.strip().split(delimiter)
                name = cols[args.cate_idx]
                try:
                    name = int(name)
                except ex:
                    pass
                finally:
                    pass
                if args.std_idx >= 0:
                    record = (float(cols[args.value_idx]), float(cols[args.std_idx]))
                else:
                    record = (float(cols[args.value_idx]), )
                data[name] = record
        data = [(c, rc) for c, rc in data.items()]
        data = sorted(data, key=lambda tp: tp[0])
        all_data[k] = data
    return all_data


def main():
    files = args.inputs.strip().split(',')
    legends = args.legends.strip().split(',')
    assert len(files) == len(legends), "inconsistent {} vs {}".format(len(files), len(legends))

    data = load_data(legends, files)

    fig, ax = plt.subplots(1, 1, figsize=(3.5, 3.5))
    for k, v in data.items():
        names = [str(tp[0]) for tp in v]
        values = [tp[1][0] for tp in v]
        if args.std_idx >= 0:
            stds = [tp[1][1] for tp in v]
            ax.errorbar(names, values, yerr=stds, uplims=True, lolims=True, label=k)
        else:
            ax.plot(names, values, label=k)
    ax.set_xlabel("number of layers")
    ax.set_ylabel("Accuracy")
    ax.legend()
    plt.tight_layout()
    plt.savefig(args.output, bbox_inches='tight')
    plt.close()


if __name__=="__main__":
    main()
