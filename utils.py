import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def get_unique_BSSIDs(dat):
   ids = []
   nscans = 0;
   fields = np.unique(dat['dat']);
   for field in fields:
      if field[0] != 's':
          ids.append(field)
      else:
          nscans += 1

   return ids, nscans


def reformat_dataframe(dat):
    tmp = dat.copy()
    curtime = 0
    times = []
    timeidx = []
    for key,val in zip(tmp['dat'], tmp['val']):
        if key[0] == 's':
            curtime += 1 
            curval = val
        times.append(curval)
        timeidx.append(curtime)
    tmp.insert(0, 'time', times,True)
    tmp.insert(0, 'timeidx', timeidx,True)

    bssid_to_ssid_map = {'null': []}
    new_ssid_label = []
    for bssid,ssid in zip(tmp['dat'], tmp['ssid']):
        if not bssid in bssid_to_ssid_map:
            bssid_to_ssid_map[bssid] = ssid
        new_ssid_label.append( bssid_to_ssid_map[bssid])

    if len(new_ssid_label) == len(tmp['ssid']):
        tmp['ssid'] = new_ssid_label

    return tmp

def deinterleave_data(dat):
    locdat = reformat_dataframe(dat)

    out = []
    tidx = np.unique( locdat['timeidx'])
    Ntimes = len(tidx)
    bssids,Nssid = get_unique_BSSIDs(locdat)
    M = -np.ones((Nssid, Ntimes))
    curssid = 0
    for bssid in bssids:
        out.append(locdat[ locdat['dat'] == bssid])
    return out


def plot_bssids(tmp, num_detects=30):
    plt.figure()
    tmin = np.array(tmp[len(tmp)-1]['time'])[0]
    for s in tmp:
       if len(s) < num_detects:
         t = np.array(s['time']).astype(float)
         t = t - tmin
         plt.plot(t, s['ssid']+'_'+s['dat'],'+')

def plot_sig_lvls(tmp, num_detects=30):
    plt.figure()
    tmin = np.array(tmp[len(tmp)-1]['time'])[0]
    for s in tmp:
       if len(s) < num_detects:
         t = np.array(s['time']).astype(float)
         t = t - tmin
         plt.plot(t, s['val'],'-+')



