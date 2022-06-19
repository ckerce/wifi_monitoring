# Traffic characterization via measurement of on-vehicle wifi temporal signal properties 

I wanted to implement a non-visul method for determing traffic volume and speed on a nearby road, with the goal of eventually combining this information with an accelerometer to allow correlation of wifi and visual data with heavy vehicles. 

The first step was to get the capture going, and determine RX antenna configurations that would generate an asymmetric directional signal. I set up airodump-ng to monitor wifi signal power levels using a reciever that can be set into monitor mode, and implemented a system to pull (signal-id, signal-power) levels once per second. I chose a dual antenna device with 1/2 wavelength spacing at 2.4 GHz and a little over 1 wavelength at 5 GHz.  Successful positioning of the antenna orientation relative to the road can be seen in the power level charts in the figure below.

I then wanted to verify that the power levels made sense from a basic physical perspective, and that they corresponded to particular vehicles.  I used a frequent passing wifi device named xpo-ltl. It turns out these are on multiple XPO Logicstics trucks, all with the same device name. I set up a security camera along the road and recorded video of the passing traffic.  I was able to verify the signal asymmetry and vehicle correlation using relatively rare good signal caputures of 6 seconds or more.  Example analysis data is show below.

![Alt text](xpo-ltl_trucks_with_wifi_signal_powers.png?raw=true) \
Figure: Two trucks passing in opposite directions within 90 seconds of each other.  Notice that the leftward signal is visible for longer regardless of which direction the truck is traveling.  This asymmetry can be used to determine travel direction purely from wifi power levels.  Note that wifi timestamps are off by 4 hours, since I did not change the time-stamp mode from PST.

![Alt text](xpo-ltl-signal_powers.png?raw=true) \
Figure:  Time series comparioson with second signal time reversed due to opposite direction of travel.

# Error calculations
The ratio of the speeds of the two trucks can be estimated from camera angles and time-to-subtend the angles.  It looks like they are traveling about the same speed, with 4:1 odds that the first truck is going faster than the second.
![Alt text](speed_calculation.png?raw=true)
