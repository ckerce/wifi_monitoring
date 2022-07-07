import os
import glob
import numpy as np
import time
import datetime
import pickle 
from matplotlib import pyplot as plt
import asyncio
import requests
import re

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
              data_struct[bssid]['times_seen'] += 1
              data_struct[bssid]['last_seen'] = last_seen
              data_struct[bssid]['new'] = False
              data_struct[bssid]['t'].append(time)
              data_struct[bssid]['chan'].append(chan)
              data_struct[bssid]['pwr'].append(pwr)
              data_struct[bssid]['ssid'].append(ssid)
       else:
           data_struct[bssid] = {}
           data_struct[bssid]['last_seen'] = time 
           data_struct[bssid]['times_seen'] = 1
           data_struct[bssid]['new'] = True 
           data_struct[bssid]['t']    = [time]
           data_struct[bssid]['chan'] = [chan]
           data_struct[bssid]['pwr']  = [pwr]
           data_struct[bssid]['ssid'] = [ssid]
    except:
        print('Bad Data: ', 'bssid: ', dat[0], ', time: ', dat[2][1:], ', chan: ', dat[3], ', pwr: ', dat[8], ', ssid: ', dat[13])

    return 0


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
    SETTREF=True 
    mac_address_list = []
    for d in dat: 
      if SETTREF:
          Tref = dat[d]['t'][0]
          SETTREF=False
      if (dat[d]['len'] < Nmax) & (dat[d]['len'] > 2) & ( (np.max(dat[d]['t']) - np.min(dat[d]['t'])) < T): 
        mac_address_list.append(d)
        plt.plot( (np.array(dat[d]['t']) - Tref) / 3600, (dat[d]['len']+1)*100 + np.array(dat[d]['pwr'])) 
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
    os.system("cp wifi_record.pickle tmp.pickle")
    time.sleep(0.1)

    with open('tmp.pickle','rb') as f:
        dat = pickle.load(f)
        for d in dat:
            dat[d]['len'] = len(dat[d]['t'])
  
    jnk = {}
    for d in dat:
       if (len(dat[d]['t']) < 100) and (len(dat[d]['t']) > 2):
          jnk[d] = dat[d]

    dat = jnk 
    mac_address_list = plot_short_wifi_hits(dat, 700, 700); plt.grid()
    plot_wifi_hits(dat)
    return mac_address_list

def cur_time_interval_flag(dat, Tstart):
    val = False
    try: 
       tdata = datetime.datetime.strptime(dat[1], ' %Y-%m-%d %H:%M:%S') 
       if tdata.timestamp() >= Tstart:
          val = True
    except:
       val = False

    return val

async def snap_reolink():
    addr = 'http://xxx.xxx.xx.xxx/cgi-bin/api.cgi?cmd=Snap&rs=blah&channel=0&user=x&password=x'
    snap_time = str(np.int(time.time())) 
    for idx in range(5):  
       response = requests.get(addr)
       with open('cap_'+snap_time+'_'+str(idx)+'.jpg', 'wb') as f:
           f.write(response.content)
           f.close()
       time.sleep(0.5)

if __name__ == '__main__':
   
   #t0 = time.time()

   p_xpo = re.compile('xpo')
   p_Keep = re.compile('Keep')
   p_Water = re.compile('Water')

   while True: #time.time() < t0 + 15:
      wifi_data = {} 
      count = 0
      Tstart = time.time()
      Tend = Tstart + 60*60
      while time.time() < Tend: 
         time.sleep(0.5)
         if len(glob.glob('outfile-01.csv')) > 0:  # allows for a restart of the airodump-ng logger 
                                                   # and deleting of files without restart of this function.
            os.system("cp outfile-01.csv tmpfile.csv")
            with open('tmpfile.csv', 'r') as csvfile:
                linenum=0
                for line in csvfile:
                  if linenum > 1:
                    dat = line.split(',')
                    if len(dat) == 15:
                        if dat[13] == '':
                            dat[13] = '--'
                        try:
                           good_update_time = (datetime.datetime.strptime(dat[1], ' %Y-%m-%d %H:%M:%S').timestamp() - Tstart > 0)
                           update_data_struct(wifi_data, dat) 
                        except:
                           good_update_time = False
                           print('                        Bad time: ', dat[1])

                        if good_update_time:
                              if dat[0] in wifi_data.keys():
                                cur_el = wifi_data[ dat[0] ]
                                if (cur_el['new'] or ((cur_el['t'][-1:][0] - cur_el['last_seen'] > 75) and cur_el['times_seen'] < 12)):
                                   cssid = cur_el['ssid'][0]
                                   print('New bssid = ', dat[0], ' ', dat[13] , '  ,  Time = ', dat[1], '   Last Seen = ', cur_el['last_seen'], '   len = ', len(wifi_data[ dat[0] ]['t']))
                                   cur_el['new'] = False
                                   if p_xpo.search(cssid) or p_Keep.search(cssid) or p_Water.search(cssid):
                                       print('Taking Snapshot :: ', cssid)
                                       asyncio.run( snap_reolink())
                  linenum+= 1
            count += 1 
            if count > 60:
              count = 0
              with open('wifi_record.pickle', 'wb') as myfile:
                 pickle.dump(wifi_data, myfile, protocol=pickle.HIGHEST_PROTOCOL)
      tmp = datetime.datetime.fromtimestamp(Tstart)
      outfile =  'airodump_'+str(np.int(Tstart))+'_'+str(tmp.year)+'_'+str(tmp.month)+'_'+str(tmp.day)+'_'+str(tmp.hour)+'_'+str(tmp.minute)+'_'+str(tmp.second)+'.pkl'
      with open(outfile, 'wb') as myfile:    
              pickle.dump(wifi_data, myfile, protocol=pickle.HIGHEST_PROTOCOL)

