import operator
import matplotlib.pyplot as plt
from pylab import *
import sys

def main():
    plt.close("all")
    fig, ax = plt.subplots()
    fns = ["D:\\v-zw\ACL2017\\NYT\\customerized\\surdeanu_provided\minzpp.tsv", "D:\\v-zw\\ACL2017\\NYT\\customerized\\surdeanu_provided\\multir.tsv", "D:\\v-zw\\ACL2017\\NYT\\customerized\\liblinear\\result_get2.tsv"]
    labelstr = ["mintz++", "multir", "mintz"]
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    markerstyle = ['s', 'o', '*', 's', 'o', '*', 's', 'o', '*', 's', 'o']
    
    for i in range(len(fns)):
        ips = open(fns[i],'r');
        precision = []
        recall = []
        for line in ips:
            eles = line[:-1].split('\t')
            precision.append(float(eles[0]))
            recall.append(float(eles[1]))
        ips.close()
        area = .0
        lastpos = recall[0]
        for j in range(len(recall)-1):
            curpos = (recall[j]+recall[j+1]) / 2
            area += (curpos-lastpos) * precision[j]
            lastpos = curpos
        area += (recall[len(recall)-1]-lastpos) * precision[len(precision)-1]
        ax.plot(recall, precision, label=(labelstr[i]+" ("+str(area)+")"), linewidth=2, color=colors[i])
        gap = len(precision) / 10
        if gap == 0:
            gap = 1
        sampleprecision = precision[0:len(precision):gap][1:]
        samplerecall = recall[0:len(recall):gap][1:]
        ax.plot(samplerecall, sampleprecision, markersize=8, marker=markerstyle[i], fillstyle="full", linestyle="none", markeredgecolor=colors[i], color=colors[i])
    lg = ax.legend(loc="upper right", shadow=True)
    frame = lg.get_frame()
    frame.set_facecolor('0.90')
    for lb in lg.get_texts():
        lb.set_fontsize('large')
    for lb in lg.get_lines():
        lb.set_linewidth(2.0)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    #plt.legend()
    plt.savefig("D:\\v-zw\\ACL2017\\NYT\\customerized\\prc.pdf")
    plt.show()
    
    
    
if __name__=="__main__":
    main()
    
