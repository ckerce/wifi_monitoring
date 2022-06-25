import os
import numpy as np
import time
import datetime
import pickle 
from matplotlib import pyplot as plt

PST_offset = 4 * 60 * 60

def convert_time(tstr):
    try:
        t = datetime.datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        t = np.nan
        print('Time format error in: ', tstr)
    return t

def update_data_struct(data_struct, dat):
    try:
       tstr = dat[2][1:]
       #t = datetime.datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')
       t = convert_time(tstr)
       t_epoch = (t - datetime.datetime(1970,1,1)).total_seconds() + PST_offset

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
    except:
        print('Bad Data: ', 'bssid: ', dat[0], ', time: ', dat[2][1:], ', chan: ', dat[3], ', pwr: ', dat[8], ', ssid: ', dat[13])

    return 0

#def get_dict_el(dat):
#    FLAG = True
#    for d in dat:
#        if FLAG:
#            out = dat[d]
#            FLAG = False
#    return out
#
#
#def split_on_time(dat_el):
#     out = []
#     ttmp = dat_el['t']
#     told = ttmp[0]
#     curwin = [told]
#     tmp = {}
#     tmp['t'] = [ told ]
#     tmp['pwr'] = [ dat_el['pwr'][0] ]
#     tmp['chan'] = [ dat_el['chan'][0] ]
#     tmp['ssid'] = [ dat_el['ssid'][0] ]
#     for v in enumerate(ttmp[1:]):
#         idx = v[0] + 1
#         t = v[1]
#         if t - told > 10: # start new track
#             tmp['len'] = len(tmp)
#             out.append(tmp) 
#             told = t
#             tmp = {}
#             tmp['t'] = [ told ]
#             tmp['pwr'] = [ dat_el['pwr'][idx] ]
#             tmp['chan'] = [ dat_el['chan'][idx] ]
#             tmp['ssid'] = [ dat_el['ssid'][idx] ]
#         else: #update current track
#             tmp['t'   ].append(t)
#             tmp['pwr' ].append( dat_el['pwr' ][idx] )
#             tmp['chan'].append( dat_el['chan'][idx] ) 
#             tmp['ssid'].append( dat_el['ssid'][idx] ) 
#             told = t
#     out.append(tmp)
#     return out 
#
#    
#def break_out_tracks(dat):
#
#    out = {}
#    for bssid in dat:
#        out[bssid] = {}
#        out[bssid]['trk'] = split_on_time(dat[bssid])
#        out[bssid]['num_trk'] = len(out[bssid]['trk'])
#    return out


def plot_wifi_hits(data_struct):
    plt.figure()
    dat = data_struct
    k=0
    for d in dat:
       #print(dat[d]['ssid'])
       curSSID = np.unique(dat[d]['ssid'])[0]
       Ntmp = len(dat[d]['ssid'])
       count_symbol = length_label( Ntmp )
       if Ntmp < 25:
          plt.plot(np.array(dat[d]['t']), Ntmp*100 + np.array(dat[d]['pwr']),'.')
          #print('chan = ',dat[d]['chan'][0], ' : pwr = ', np.min([-10.0,np.round(np.average(dat[d]['pwr']))]), ' : count = ', Ntmp, ' ', count_symbol,  ' : ', curSSID)
       k+=1

def length_label(n):
    pad = '             '
    sym = ']]]]]]]]]]]]]]'
    out = sym[0:n]+pad[n:]
    return out

def plot_short_wifi_hits(data_struct, T=30, Nmax=60):
    plt.figure() 
    k=0 
    dat = data_struct 
    mac_address_list = []
    for d in dat: 
      if (dat[d]['len'] < Nmax) & (dat[d]['len'] > 2) & ( (np.max(dat[d]['t']) - np.min(dat[d]['t'])) < T): 
        mac_address_list.append(d)
        plt.plot(np.array(dat[d]['t']), (dat[d]['len']+1)*100 + np.array(dat[d]['pwr'])) 
        curSSID = np.unique(dat[d]['ssid'])[0]
        Ntmp = len(dat[d]['ssid'])
        count_symbol = length_label( Ntmp )
        print('time = ', datetime.datetime.fromtimestamp(dat[d]['t'][0]), ' : chan = ', dat[d]['chan'][0], ' : pwr = ', np.min([-10.0,np.round(np.average(dat[d]['pwr']))]), ' : count = ', Ntmp, ' ', count_symbol,  ' : ', curSSID) 
        k+=1 
    return mac_address_list 

def plot_intermediate_wifi_hits(data_struct,T=30):
    plt.figure()
    k=0
    dat = data_struct
    for d in dat:
      if (dat[d]['len'] < 150) & (dat[d]['len'] > 5) & ( (np.max(dat[d]['t']) - np.min(dat[d]['t'])) < T):
        plt.plot(np.array(dat[d]['t']), np.array(dat[d]['pwr']),'.')
        print(dat[d]['ssid'])
        k+=1


def display_results():
    os.system("cp wifi_record.txt tmp.txt")
    time.sleep(0.1)

    with open('tmp.txt','rb') as f:
        dat = pickle.load(f)
        for d in dat:
            dat[d]['len'] = len(dat[d]['t'])
   
   
    mac_address_list = plot_short_wifi_hits(dat, 700); plt.grid()
    plot_wifi_hits(dat)
    return mac_address_list

if __name__ == '__main__':
   wifi_data = {} 
   count = 0
   for i in range(24*2*3600):
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
      if count > 15:
        count = 0
        with open('wifi_record.txt', 'wb') as myfile:
           pickle.dump(wifi_data, myfile, protocol=pickle.HIGHEST_PROTOCOL)
      
