#!/usr/bin/python3

import socket,select,time,sys,argparse

class bcolors:  
	ENDC = '\033[0m'
	RED = '\033[31m'
	BLU = '\033[34m'
	CYAN = '\033[96m'
	
ports = []         #Listening Ports
socklist = []      #List of client sockets
relay = {}         #Dict of sckets with connecting port
socks = {}         #Dict of all the listening sockets
s = select.select

#Accepts the connection from the client and connects back to the client on the originating port
def xaccept(s, port):
	sock, addr = s.accept()
	print(bcolors.BLU+'[+]'+bcolors.ENDC+'Connection from: %s:%s -> port:%s' % (addr[0],addr[1],port))
	client = (addr[0], port)
	reflector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:   #Try connecting back to the client
		reflector.connect((client[0], client[1]))
	except:
		return
	if reflector:   # If the connection was successful save the connection info in to a lit and dict         
		socklist.append(sock)
		socklist.append(reflector)
		relay[sock] = reflector
		relay[reflector] = sock
	else:          
		clientsock.close()

#send data through the relay
def xrecv(data,s):
	relay[s].send(data)	   #Sends the data	

#closes the connecion
def xclose(s):
	discon = s.getpeername()
	print(bcolors.RED+'[-]'+bcolors.ENDC+'Disconnected from %s:%s' % (discon[0],discon[1]))
	fin = relay[s]
	socklist.remove(s)
	socklist.remove(fin)
	relay[fin].close()               #closes the connection of one part of relay
	done.close()                     #closes the connection of the other part of the relay
	del relay[fin]
	del fin

#argument Parser
arg = argparse.ArgumentParser()
arg.add_argument("-p", "--ports", dest = "ports", help="Listening Ports", default="x")
args = arg.parse_args()

#If no ports the print usage
if len(sys.argv) == 1 or args.ports == "x":
	print("Usage python3 reverberate.py -p 22,53,80")
	exit()
else:
	portinput = args.ports.split(',')
	for z in portinput:
		ports.append(int(z))

#For each port in arg, open a listening socket
for x in ports:
	socks[x] = socket.socket()                       
	socks[x].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		socks[x].bind(('', x))       
		print(bcolors.CYAN+"[*]"+bcolors.ENDC+"socket binded to %s" % (x))
		socks[x].listen(5)            
		socklist.append(socks[x])
	except:
		print("Port %s is in use, try again using another port" % x)
		exit()
		
#While true connect to any socket that trys to connect and relay any info received
while True:
	rlist, wlist, xlist = s(socklist, [], [])
	for y in ports: 
		if str(y) in str(rlist) and "raddr" not in str(rlist):
			connect = socks[y]
			port = y
	for i in rlist:  #if there is a connection to any of the open ports accept and try to connect back
		if i == connect:
			xaccept(i,port)
			break
		try:   #If received data send on through the relay in not close
			data = i.recv(4096)
			if len(data) == 0:
				xclose(i)
				break
			else:
				xrecv(data,i) 
		except:
			pass