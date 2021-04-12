from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import argparse
import os
import math

import yaml
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

parser = argparse.ArgumentParser(description='Draw beeswarm graph')
parser.add_argument('indir',
                    type=str,
                    help='folder to load data')
parser.add_argument("outpath", type=str, help="path of saved figure")
parser.add_argument("--schema", type=str, default=None, help="e.g., graph_type,pooling,optimizer,feature,trial")
parser.add_argument("--filter", type=str, default="", help="considered values")
parser.add_argument("--metric", type=str, default="", help="metric of interest, e.g., extrapolate_mape")
parser.add_argument("--metric-name", type=str, default="", help="the name of the metric of interest, e.g., MAPE")
parser.add_argument("--cmp-col", type=str, default="pooling", help="the name of the column of interest")
parser.add_argument("--except-threshold", type=float, default=None, help="remind and filter out exceptional data")
args = parser.parse_args()


def main():
    if args.schema:
        schema = args.schema.strip().split(',')
    else:
        schema = None
    considered_values = args.filter.split(',')

    tabular_data = list()
    #tabular_data.append(schema+[args.metric])

    if os.path.isdir(args.indir):
        _, dirs, filenames = next(os.walk(args.indir))
        print(dirs)
        for fd in dirs:
            rcd = fd.split('_')
            if len(rcd) == len(schema):
                if len(considered_values) == len(schema):
                    skip = False
                    for realization, considered in zip(rcd, considered_values):
                        if considered and ((considered[0] != '~' and realization != considered) or (considered[0] == '~' and realization == considered[1:])):
                            skip = True
                            break
                fn = os.path.join(args.indir, fd, 'results.yaml')
                with open(fn, 'r') as ips:
                    results = yaml.load(ips)
                if math.isnan(results[args.metric]):
                    print("{} results in {}=nan".format(rcd, args.metric))
                    continue
                tabular_data.append(rcd+[results[args.metric]])
            else:
                # have many trials
                _, subdirs, _ = next(os.walk(os.path.join(args.indir, fd)))
                for subfd in subdirs:
                    trial_id = subfd[6:]
                    if len(considered_values) == len(schema):
                        skip = False
                        for realization, considered in zip(rcd+[trial_id], considered_values):
                            if considered and ((considered[0] != '~' and realization != considered) or (considered[0] == '~' and realization == considered[1:])):
                                skip = True
                                break
                        if skip:
                            continue
                    fn = os.path.join(args.indir, fd, subfd, 'results.yaml')
                    with open(fn, 'r') as ips:
                        results = yaml.load(ips)
                    if math.isnan(results[args.metric]):
                        print("{} results in {}=nan".format(rcd, args.metric))
                        continue
                    tabular_data.append(rcd+[trial_id]+[results[args.metric]])
    else:
        # specified a csv/tsv file containing all the necessary results
        with open(args.indir, 'r') as ips:
            delimiter = ',' if args.indir.endswith("csv") else '\t'
            is_first_line = True
            check_col = None
            for line in ips:
                if is_first_line:
                    if schema is None:
                        schema = line.strip().split(delimiter)
                        if args.except_threshold:
                            check_col = schema.index(args.metric_name)
                    is_first_line = False
                    continue
                vals = line.strip().split(delimiter)
                for i, v in enumerate(vals):
                    try:
                        new_v = float(v)
                        vals[i] = new_v
                    except Exception as ex:
                        pass
                    finally:
                        pass
                if check_col is not None:
                    if vals[check_col] >= args.except_threshold:
                        print(vals)
                        continue
                tabular_data.append(vals)

    tabular_data = pd.DataFrame(tabular_data, columns=schema + ([args.metric_name] if args.metric else []))
    print(tabular_data)

    sns.set_theme(style="whitegrid")
    ax = sns.violinplot(x=args.cmp_col, y=args.metric_name, data=tabular_data, inner=None)
    ax = sns.swarmplot(x=args.cmp_col, y=args.metric_name, data=tabular_data, color="white", edgecolor="gray")
    plt.tight_layout()
    plt.savefig(args.outpath, bbox_inches='tight')
    plt.close()


if __name__=="__main__":
    main()
