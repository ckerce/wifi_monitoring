
dat = pd.read_csv('working.csv')

tmp = deinterleave_data(dat)

for s in tmp: 
    if len(s) < 9000: 
       t = np.array(s['time']).astype(float) 
       t = t - tmin 
       plt.plot(t,s['ssid']+'___'+s['dat'],'+') 

