Datatracker for RadsatG
-----------------------


This code was designed to decode the data coming from MSU's Radsatg cubesatellite.  A gui writting with python tkinter will run and populate the entries upon receiving data from the TCP connection to the ground computer.  

The ground computer will receive the signal at a doppler shifted 437.425MHz with a AX.25 packet from a Astrodev Lithium 2 radio.  The modulation method is GMSK with a baud of 19.2k/baud.


