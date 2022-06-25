def split_on_time(dat_el):
     out = []
     ttmp = dat_el['t']
     told = ttmp[0]
     curwin = [told]
     tmp = {}
     tmp['t'] = [ told ]
     tmp['pwr'] = [ dat_el['pwr'][0] ]
     tmp['chan'] = [ dat_el['chan'][0] ]
     tmp['ssid'] = [ dat_el['ssid'][0] ]
     for v in enumerate(ttmp[1:]):
         idx = v[0] + 1
         t = v[1]
         if t - told > 30: # start new track if more than 30 seconds has passes since last detection
             tmp['len'] = len(tmp)
             out.append(tmp) 
             told = t
             tmp = {}
             tmp['t'] = [ told ]
             tmp['pwr'] = [ dat_el['pwr'][idx] ]
             tmp['chan'] = [ dat_el['chan'][idx] ]
             tmp['ssid'] = [ dat_el['ssid'][idx] ]
         else: #update current track
             tmp['t'   ].append(t)
             tmp['pwr' ].append( dat_el['pwr' ][idx] )
             tmp['chan'].append( dat_el['chan'][idx] ) 
             tmp['ssid'].append( dat_el['ssid'][idx] ) 
             told = t
     out.append(tmp)
     return out   
    
    
def break_out_tracks(dat):
   
    out = {}
    for bssid in dat:
        out[bssid] = {}
        out[bssid]['trk'] = split_on_time(dat[bssid])
        out[bssid]['num_trk'] = len(out[bssid]['trk'])
    return out

def print_passes(ddat, min_passes=2, max_passes=100):
    trk_count = 0
    for idx in range(min_passes,max_passes):
      for d in ddat:
        if ddat[d]['num_trk'] == idx:
          trk_count += 1
          print('Trk: ', trk_count, '  :  ,', ' Num Passes = ', idx, '  :  ', ddat[d]['trk'][0]['ssid'][0])
