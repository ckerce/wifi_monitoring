import os
import numpy as np
import time
import datetime
import pickle 
from matplotlib import pyplot as plt


def update_data_struct(data_struct, dat):
    tstr = dat[2][1:]
    t = datetime.datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')
    t_epoch = (t - datetime.datetime(1970,1,1)).total_seconds()

    bssid = dat[0]
    time = t_epoch
    chan = np.int8(dat[3])
    pwr  = np.float(dat[8])
    ssid = dat[13]

    if bssid in data_struct.keys():
        last_seen = data_struct[bssid]['t'][-1:][0]
        if time > last_seen:
           data_struct[bssid]['t'].append(time)
           data_struct[bssid]['chan'].append(chan)
           data_struct[bssid]['pwr'].append(pwr)
           data_struct[bssid]['ssid'].append(ssid)
    else:
        data_struct[bssid] = {}
        data_struct[bssid]['t']    = [time]
        data_struct[bssid]['chan'] = [chan]
        data_struct[bssid]['pwr']  = [pwr]
        data_struct[bssid]['ssid'] = [ssid]
    return 0

def plot_wifi_hits(data_struct):
    plt.figure()
    dat = data_struct
    k=0
    for d in dat:
       plt.plot(np.array(dat[d]['t']), 100*k + np.array(dat[d]['pwr']),'.')
       print(dat[d]['ssid'])
       k+=1

def length_label(n):
    pad = '             '
    sym = ']]]]]]]]]]]]]]'
    out = sym[0:n]+pad[n:]
    return out

def plot_short_wifi_hits(data_struct, T=30):
    plt.figure() 
    k=0 
    dat = data_struct 
    for d in dat: 
      if (dat[d]['len'] < 120) & (dat[d]['len'] > 0) & ( (np.max(dat[d]['t']) - np.min(dat[d]['t'])) < T): 
        plt.plot(np.array(dat[d]['t']), (dat[d]['len']+1)*100 + np.array(dat[d]['pwr'])) 
        curSSID = np.unique(dat[d]['ssid'])[0]
        Ntmp = len(dat[d]['ssid'])
        count_symbol = length_label( Ntmp )
        print('chan = ',dat[d]['chan'][0], ' : pwr = ', np.round(np.average(dat[d]['pwr'])), ' : count = ', Ntmp, ' ', count_symbol,  ' : ', curSSID) 
        k+=1 

def plot_intermediate_wifi_hits(data_struct,T=30):
    plt.figure()
    k=0
    dat = data_struct
    for d in dat:
      if (dat[d]['len'] < 50) & (dat[d]['len'] > 5) & ( (np.max(dat[d]['t']) - np.min(dat[d]['t'])) < T):
        plt.plot(np.array(dat[d]['t']), np.array(dat[d]['pwr']),'.')
        print(dat[d]['ssid'])
        k+=1


if __name__ == '__main__':
   wifi_data = {} 
   count = 0
   for i in range(6*2*3600):
      os.system("cp outfile-01.csv tmpfile.csv")
      time.sleep(0.5)
      with open('tmpfile.csv', 'r') as csvfile:
          linenum=0
          for line in csvfile:
            if linenum > 1:
              dat = line.split(',')
              if len(dat) == 15:
                  if dat[13] == '':
                      dat[13] = '--'
                  update_data_struct(wifi_data, dat) 
            linenum+= 1
      count += 1 
      if count > 100:
        count = 0
        with open('wifi_record.txt', 'wb') as myfile:
           pickle.dump(wifi_data, myfile, protocol=pickle.HIGHEST_PROTOCOL)
      
