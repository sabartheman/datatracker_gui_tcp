import socket
UDP_PORT = 3000
interface=""

sock = socket.socket(socket.AF_INET, # Ethernet
                     socket.SOCK_DGRAM) # UDP

sock.bind((interface, UDP_PORT))

while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print ("received message:{0}".format(data))
