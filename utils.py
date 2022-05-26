import pandas as pd
import numpy as np

def get_unique_SSIDs(dat):
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
    return tmp

def deinterleave_data(dat):
    locdat = reformat_dataframe(dat)

    out = []
    tidx = np.unique( locdat['timeidx'])
    Ntimes = len(tidx)
    ssids,Nssid = get_unique_SSIDs(locdat)
    M = -np.ones((Nssid, Ntimes))
    curssid = 0
    for ssid in ssids:
        out.append(locdat[ locdat['dat'] == ssid])
    return out


def make_plots(dat):
    tmp = deinterleave_data(dat)
    for s in tmp:
    if len(s) < 500:
       t = np.array(s['time']).astype(float)
       t = t - tmin
       plt.plot(t, s['val']+'_'+s['dat'],'+')





