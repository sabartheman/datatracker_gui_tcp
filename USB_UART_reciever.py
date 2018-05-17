import time
import serial
import logging
import datetime
import threading

#setting up a logging unit to take in all the data
#in a semi-neat way
logger = logging.getLogger("benchtop")
hdlr = logging.FileHandler('benchtop.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

testtext = open("testtext.txt", "w")

#setting up the uart port
USB = serial.Serial("COM4", 115200,timeout=.1)

#defining what should be global vars

global data
global count
global threadrun
global datarecieved

#defining what are the global values
data = b'\xcc\xcc\xdc'

threadrun = True
datarecieved = False

count = 0



class readUART(threading.Thread):
    def run(self):
        print("going to try and read from the UART port")
        global threadrun
        global datarecieved
        global data
        USB.reset_input_buffer()
        while(threadrun):
            try:
                data = USB.readline(1024)
                datarecieved = True
                if(len(data) > 40):
                    print(f"length of data: {len(data)}, data: {data}" )

            except:
                testtext.close()
                print("stopping uart read because of exception")
                USB.close()
                exit()

class recordData(threading.Thread):
    def run(self):
        global threadrun
        global count
        global datarecieved
        global data
        while(threadrun):
            if(datarecieved):
                #making sure there isn't a repeat of data coming in
                datarecieved = False
                #testtext.write(data)
                if(len(data) > 40):

                    print("Data recieved: " + str(data))
                    count = count + 1
                    print(f"logging data, length: {len(data)}, Count: {count}")
                    logger.info(len(data))
                    logger.info(data)
                    #resetting the data back to a test figure so that it doesn't
                    #record multiple times into the log file
                    data = b'\xcc\xcc\xdc'






if __name__ == '__main__':
    try:
        readingtime = readUART()
        writingtime = recordData()

        USB.reset_input_buffer()
        readingtime.start()
        writingtime.start()
        #need a no-op command to keep the program from running away?
        while(True):
            pass

    #doesn't seem to work
    except:
        print("\n \n \nexception called, exiting program")
        USB.close()
        print("USB closed and program exiting")
        threadrun = False
        readingtime.join()
        writingtime.join()
        print("Both of the threads have been cleaned up")

        exit()
