from utils import *
import pandas as pd
from argparse import ArgumentParser


if __name__ == '__main__': 
    parser = ArgumentParser() 
    parser.add_argument('-f','--file', help = 'Input wifi scanning file.') 
    args = parser.parse_args() 

    wifi_scan_file = args.file
    dat = pd.read_csv(wifi_scan_file) 
    tmp = deinterleave_data(dat) 

    Nmax = len(dat) 
    Ncar = 10 

    plt.ion() 
    plot_bssids(tmp,Nmax) 
    plot_bssids(tmp,Ncar) 
    plot_sig_lvls(tmp,Nmax) 
    plot_sig_lvls(tmp,Ncar)

