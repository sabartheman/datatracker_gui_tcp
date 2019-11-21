import socket
import sys
import datetime



TCP_IP   = """(enter up in string here)"""
TCP_PORT = 3000
BUFFERSIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_address = ("""(enter up in string here)""", 3000)
sock.connect(server_address)

#print(sock.listen(1))






def main():
    while(True):
        try:
            now = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            s.connect((TCP_IP, TCP_PORT))
            data = s.recv(BUFFERSIZE)
            s.close()
            print("--------------------------------------")
            print("       " + now + "       ")
            print("--------------------------------------")
            print(len(data))
            #seperating the different tiers of data
            if(len(data) == 96):
                print("Tile data")
                print("{}".format(data))
            elif(len(data) == 208):
                print("Health data")
                print("{}".format(data))
            elif(len(data) == 215):
                print("Power data")
                print("{}".format(data))
            else:
                print("Miscellaneous data")
                print("{}".format(data))


        except KeyboardInterrupt:
            print("should be exitiing")
            s.close()
            break



if __name__ == "__main__":
    main()
    print("finished")
