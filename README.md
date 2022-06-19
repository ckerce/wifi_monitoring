# Traffic characterization via measurement of on-vehicle wifi temporal signal properties 

I wanted to implement a non-visul method for determing traffic volume and speed on a nearby road, with the goal of eventually combining this information with an accelerometer to allow correlation of wifi and visual data with heavy vehicles. 

The first step was to get the capture going, and determine RX antenna configurations that would generate an asymmetric directional signal. I set up airodump-ng to monitor wifi signal power levels using a reciever that can be set into monitor mode, and implemented a system to pull (signal-id, signal-power) levels once per second. I chose a dual antenna device with 1/2 wavelength spacing at 2.4 GHz and a little over 1 wavelength at 5 GHz.  Successful positioning of the antenna orientation relative to the road can be seen in the power level charts in the figure below.

I then wanted to verify that the power levels made sense from a basic physical perspective, and that they corresponded to particular vehicles.  I used a frequent passing wifi device named xpo-ltl. It turns out these are on multiple XPO Logicstics trucks, all with the same device name. I set up a security camera along the road and recorded video of the passing traffic.  I was able to verify the signal asymmetry and vehicle correlation using relatively rare good signal caputures of 6 seconds or more.  Example analysis data is show below.

![Alt text](xpo-ltl_trucks_with_wifi_signal_powers.png?raw=true) \
Figure 1: Two trucks passing in opposite directions within 90 seconds of each other.  Notice that the leftward signal is visible for longer regardless of which direction the truck is traveling.  This asymmetry can be used to determine travel direction purely from wifi power levels.  Note that wifi timestamps are off by 4 hours, since I did not change the time-stamp mode from PST.

![Alt text](xpo-ltl-signal_powers.png?raw=true) \
Figure 2:  Time series comparioson with second signal time reversed due to opposite direction of travel.

# Video-derived relative speed and error calculations
Looking at Figure 2, it is tempting to thing that velocity might be derived from the shape of the wifi power curves under the assumption that the TX power does not fluctuate of the capture duration.  While this is likely true, the story is a bit nuanced due to the different distances between lanes and reciever.  Casual analysis of Figure 2 might lead one to think that truck 1 is going significantly faster than truck 2.  An analysis of some of the issues follows.   

The wifi signal strength and RX power is dependent on the TX/RX geometry, with distance being a primary factor.  There is no obvious absolute observable in the video data that does not have large measurement error. For example the wheelbase of different trucks is the same, so wheel-to-wheel displacement time is independent of sensor-truck distand and angle.  Even without knowing the absolue lengths of the trucks, the standard container sizes could be used as a distance unit to determine relative speed ratio, which is independent of units.  However, the time granularity of the image captures is about 250 ms, which creates very large errors in the "container length unit" system over the timescales of interest (much less than 1000 ms).  It makes more sense to us large subtended angles, where measurements are on the order of 10,000 ms.   

Taking the approach that the ratio of the speeds of the two trucks can be estimated from camera angles and time-to-subtend the angles, the notes below show the geometry and algebraic relationships for relative velocity measurements in terms of measurable times and distances.  Following those formulae, it looks like the two trucks are traveling about the same speed, with 4:1 odds that the first truck is going faster than the second.  Rough calculations are that the first truck is traveling about 10% faster than the second, but the velocity ratio standard deviation is around 5.5%. \
![Alt text](speed_calculations.png?raw=true)
