import time
import serial
import logging
import datetime
import threading

USB = serial.Serial("COM4", 115200,timeout=0.1)

charArray = b'He'

class readSingle(threading.Thread):
    #With our current setup in the lab we cannot use the readline method
    #will not capture the data that we want.


    def run(self):
        try:
            while(True):
                data = USB.readline(2)
                #print(f"{data}")
                if(data == b'He'):
                    #datastring = USB.read(6)        #get rid of radio header
                    charArray = b'He' + USB.read(210)
                    now = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
                    print(f"{now}\nlength {len(charArray)}, data: {charArray.hex()}\n")
                    charArray = b'He'

        except:
            USB.close()
            exit()



if __name__ == '__main__':
    try:
        singlechar = readSingle()
        singlechar.run()

    except:
        USB.close()
        exit()
