# reverberate
reverberate.py is a program that reflects or relays a connection back to the originator.
It is designed to open up ports on a machine and if device connects to it, it will then 
try and connect back to the device using the same port and relay the info back.
It would be like talking to a mirror...

Usage:
For a single port:
python3 reverberate.py -p 22

For multi ports:
python3 reverberate.py -p 22,53,80

