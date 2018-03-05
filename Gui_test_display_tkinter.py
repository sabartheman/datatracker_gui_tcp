#   Author: Skylar Tamke
#   with help from:  Johnny Gaddis
#
#
#

import sys
import socket
import datetime
import threading
from tkinter import *
from time import sleep

test_string_health = b'\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x13\x00\x00\x00{\xdc3\x1d\x10\x1dB\x1d\x9e\x00\x00\x0c\xea\x0c\xe2\x0c\xea\x0c\xd7\t\xc1\t\xca\t\xd6\t\xbf\x07\x07\x07\x07\x07\x0c\x06\xfa\x03\xe1\x03\xe7\x03\xf1\x03\xda\x03\xb5\x03\xb6\x03\xbb\x03\xb2\t\xc4\t\xa7\n`\x00\x00\x02q\x02q\x02q\x02q\x07\xef\x08r\t\xc4\x07S\x04\xe2\x04\x86\x04\xe2\x04E\x06\xb6\x05\xcd\x06\xb6\x04\xe2\x08\x8b\x08\x8b\x08\x8b\x08\x8b}\xfajR\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x1b\x00\x00\x00%\xcc\xcc\xdc'

test_string_tile = b'\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00J\xdc\x88\x00\x00\xd7\xe8\x02\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf8\x03\x00\x00\x00\x00\x00\x00\x07\xeb\x07\xeb\x07\xeb\x00\x03\xcc\xcc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdc\x00\x00\x00\x00\x00\x00\xc0'

test_string_power = b'\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdb\xdc\x00\x00e\xb7\x00\x00\n\xe2\x00\xc5\x00\xc5\x00\x00\x00\x00\x00\x00\x00\x03\x00\xac\x00\x00\x00\x00\x03\xa7\x02o\x02\x18\x02\x14\x01\xc9\x01\xbf\x02p\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00>\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc4\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x0e\x01\x08\x01\x0c\x01\x08\x01\x0c\x01\x08\x02\x13\x02\x19\x02\x12\x02\x17\x02\x12\x02\x19\x81\xff\x82\x00\x81\xf8\x82\x00\x81\xff\x81\xf4S\xb6\xdb\xdc\xdb\xdc\xdb\xdc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0'



TCP_IP   = "153.90.121.248"
TCP_PORT = 3000
BUFFERSIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_address = ('153.90.121.248', 3000)
sock.connect(server_address)


class DataGui(Frame):

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.root = parent
        self.root.title("Data Gui")

        self.grid(column=0,row=0, sticky='nsew')


        self.timevar = StringVar()
        self.timevar.set("test")
        self.clock()

        Label(self,height=3,bg="white", text="Time: ").grid(row=1, column=1,sticky=W)
        Label(self,height=3,bg="white", text="Last Recieved: ").grid(row=1, column=3,sticky=W)


        Label(self, text="Tile data: ").grid(row=5, column=1,sticky=W)
        Label(self,justify=LEFT,wraplength=400, text=test_string_tile.hex()).grid(row=5, column=2, sticky=W)
        Label(self, text=" ").grid(row=7, column=2,sticky=W)


        Label(self, text="Health data: ").grid(row=10, column=1, sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=test_string_health.hex()).grid(row=10, column=2,sticky=W)
        Label(self, text=" ").grid(row=12, column=2,sticky=W)


        #Label(self, text="Power data: ").grid(row=16, column=1, sticky=W)
        Label(self, text="Bytes Sent: ").grid(row=16, column=1, sticky=W)
        Label(self, text="Bytes Recv: ").grid(row=16, column=3, sticky=W)
        Label(self, text="PKTS Sent: ").grid(row=17, column=1, sticky=W)
        Label(self, text="PKTS Recv: ").grid(row=17, column=3, sticky=W)
        Label(self, text="Invld Pack: ").grid(row=18, column=1, sticky=W)
        Label(self, text="CRC  Fails: ").grid(row=18, column=3, sticky=W)
        Label(self, text="status  : ").grid(row=19, column=1, sticky=W)
        Label(self, text="Reset flag: ").grid(row=19, column=3, sticky=W)

        Label(self, text="SA1_BOOST_V: ").grid( row=20, column=1, sticky=W)
        Label(self, text="SA1_V: ").grid(       row=20, column=3, sticky=W)
        Label(self, text="SA2_BOOST_V: ").grid( row=21, column=1, sticky=W)
        Label(self, text="SA2_V: ").grid(       row=21, column=3, sticky=W)
        Label(self, text="SA3_V: ").grid(       row=22, column=1, sticky=W)
        Label(self, text="SA3_BOOST_V: ").grid( row=22, column=3, sticky=W)

        Label(self, text="BATT2_TEMP: ").grid(row=23, column=1, sticky=W)
        Label(self, text="BATT1_TEMP: ").grid(row=23, column=3, sticky=W)

        Label(self, text="5V0BUS_V: ").grid(row=23, column=5, sticky=W)
        Label(self, text="3V3BUS_V: ").grid(row=23, column=7, sticky=W)

        Label(self, text="VBATT2_V: ").grid(row=24, column=1, sticky=W)
        Label(self, text="VBATT_V : ").grid(row=24, column=3, sticky=W)
        Label(self, text="VBATT1_V: ").grid(row=24, column=5, sticky=W)

        Label(self, text="3V3BUS_TEMP: ").grid(row=25, column=1, sticky=W)
        Label(self, text="5V0BUS_TEMP: ").grid(row=25, column=3, sticky=W)

        Label(self, text="3V3EPS_V   : ").grid(row=25, column=5, sticky=W)

        Label(self, text="SA1_I: ").grid(row=26, column=1, sticky=W)
        Label(self, text="SA2_I: ").grid(row=26, column=3, sticky=W)
        Label(self, text="SA3_I: ").grid(row=26, column=5, sticky=W)

        Label(self, text="DISCHARGE_I: ").grid(row=27, column=1, sticky=W)
        Label(self, text="CHARGE_I   : ").grid(row=27, column=3, sticky=W)
        Label(self, text="3V3BUS_I   : ").grid(row=27, column=5, sticky=W)
        Label(self, text="VBATT1_I   : ").grid(row=27, column=7, sticky=W)
        Label(self, text="VBATT2_I   : ").grid(row=27, column=9, sticky=W)

        Label(self, text="SA_Ym_TEMP: ").grid(row=28, column=1, sticky=W)
        Label(self, text="SA_Zp_TEMP: ").grid(row=28, column=3, sticky=W)
        Label(self, text="SA_Zm_TEMP: ").grid(row=28, column=5, sticky=W)
        Label(self, text="SA_Xp_TEMP: ").grid(row=28, column=7, sticky=W)
        Label(self, text="SA_Yp_TEMP: ").grid(row=28, column=9, sticky=W)

        Label(self, text="3V3EPS_I: ").grid(row=29, column=1, sticky=W)
        Label(self, text="5V0BUS_I: ").grid(row=29, column=3, sticky=W)

        Label(self, text="HIST_SA_1_P_1: ").grid(row=30, column=1, sticky=W)
        Label(self, text="HIST_SA_1_P_2: ").grid(row=30, column=3, sticky=W)
        Label(self, text="HIST_SA_1_P_3: ").grid(row=30, column=5, sticky=W)
        Label(self, text="HIST_SA_1_P_4: ").grid(row=30, column=7, sticky=W)
        Label(self, text="HIST_SA_1_P_5: ").grid(row=30, column=9, sticky=W)
        Label(self, text="HIST_SA_1_P_6: ").grid(row=30, column=11, sticky=W)

        Label(self, text="HIST_SA_2_P_1: ").grid(row=31, column=1, sticky=W)
        Label(self, text="HIST_SA_2_P_2: ").grid(row=31, column=3, sticky=W)
        Label(self, text="HIST_SA_2_P_3: ").grid(row=31, column=5, sticky=W)
        Label(self, text="HIST_SA_2_P_4: ").grid(row=31, column=7, sticky=W)
        Label(self, text="HIST_SA_2_P_5: ").grid(row=31, column=9, sticky=W)
        Label(self, text="HIST_SA_2_P_6: ").grid(row=31, column=11, sticky=W)

        Label(self, text="HIST_SA_3_P_1: ").grid(row=32, column=1, sticky=W)
        Label(self, text="HIST_SA_3_P_2: ").grid(row=32, column=3, sticky=W)
        Label(self, text="HIST_SA_3_P_3: ").grid(row=32, column=5, sticky=W)
        Label(self, text="HIST_SA_3_P_4: ").grid(row=32, column=7, sticky=W)
        Label(self, text="HIST_SA_3_P_5: ").grid(row=32, column=9, sticky=W)
        Label(self, text="HIST_SA_3_P_6: ").grid(row=32, column=11, sticky=W)

        Label(self, text="HIST_BATT_V_1: ").grid(row=33, column=1, sticky=W)
        Label(self, text="HIST_BATT_V_2: ").grid(row=33, column=3, sticky=W)
        Label(self, text="HIST_BATT_V_3: ").grid(row=33, column=5, sticky=W)
        Label(self, text="HIST_BATT_V_4: ").grid(row=33, column=7, sticky=W)
        Label(self, text="HIST_BATT_V_5: ").grid(row=33, column=9, sticky=W)
        Label(self, text="HIST_BATT_V_6: ").grid(row=33, column=11, sticky=W)

        Label(self, text="HIST_BATT_I_1: ").grid(row=34, column=1, sticky=W)
        Label(self, text="HIST_BATT_I_2: ").grid(row=34, column=3, sticky=W)
        Label(self, text="HIST_BATT_I_3: ").grid(row=34, column=5, sticky=W)
        Label(self, text="HIST_BATT_I_4: ").grid(row=34, column=7, sticky=W)
        Label(self, text="HIST_BATT_I_5: ").grid(row=34, column=9, sticky=W)
        Label(self, text="HIST_BATT_I_6: ").grid(row=33, column=11, sticky=W)

        self.updatePower(test_string_health)

        Label(self, text="Misc data/Powerchunk: ").grid(row=100, column=1, sticky=W)


    def updateTile(self,data):
        Label(self, justify=LEFT, wraplength=400, text=data.hex()).grid(row=5, column=2,sticky=W)

    def updateHealth(self,data):
        Label(self, justify=LEFT, wraplength=400, text=data.hex()).grid(row=10, column=2,sticky=W)

    def updatePower(self,data):
        DATAOFFSET = 29

        Label(self, justify=LEFT, wraplength=800, text=str(int(data[1+DATAOFFSET:4+DATAOFFSET].hex(),16))).grid(row=16, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[5+DATAOFFSET:8+DATAOFFSET].hex(),16))).grid(row=16, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[9+DATAOFFSET:10+DATAOFFSET].hex()).grid(row=17, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[11+DATAOFFSET:12+DATAOFFSET].hex()).grid(row=17, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[13+DATAOFFSET:14+DATAOFFSET].hex()).grid(row=18, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[15+DATAOFFSET:16+DATAOFFSET].hex()).grid(row=18, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[17+DATAOFFSET:18+DATAOFFSET].hex()).grid(row=19, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[19+DATAOFFSET:20+DATAOFFSET].hex()).grid(row=19, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[21+DATAOFFSET:22+DATAOFFSET].hex()).grid(row=20, column=2,sticky=W)

        #SA1 SA2 SA3
        Label(self, justify=LEFT, wraplength=800, text=data[23+DATAOFFSET:24+DATAOFFSET].hex()).grid(row=20, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[25+DATAOFFSET:26+DATAOFFSET].hex()).grid(row=20, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[27+DATAOFFSET:28+DATAOFFSET].hex()).grid(row=21, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[29+DATAOFFSET:30+DATAOFFSET].hex()).grid(row=21, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[31+DATAOFFSET:32+DATAOFFSET].hex()).grid(row=22, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[33+DATAOFFSET:34+DATAOFFSET].hex()).grid(row=22, column=4,sticky=W)

        #BATT TEMPS
        Label(self, justify=LEFT, wraplength=800, text=data[35+DATAOFFSET:36+DATAOFFSET].hex()).grid(row=23, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[37+DATAOFFSET:38+DATAOFFSET].hex()).grid(row=23, column=4,sticky=W)

        #BUS VOLTAGE
        Label(self, justify=LEFT, wraplength=800, text=data[39+DATAOFFSET:40+DATAOFFSET].hex()).grid(row=23, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[41+DATAOFFSET:42+DATAOFFSET].hex()).grid(row=23, column=8,sticky=W)

        #BATTERY VOLTAGE
        Label(self, justify=LEFT, wraplength=800, text=data[43+DATAOFFSET:44+DATAOFFSET].hex()).grid(row=24, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[45+DATAOFFSET:46+DATAOFFSET].hex()).grid(row=24, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[47+DATAOFFSET:48+DATAOFFSET].hex()).grid(row=24, column=6,sticky=W)

        #BUS TEMPS
        Label(self, justify=LEFT, wraplength=800, text=data[49+DATAOFFSET:50+DATAOFFSET].hex()).grid(row=25, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[51+DATAOFFSET:52+DATAOFFSET].hex()).grid(row=25, column=4,sticky=W)

        #3V3EPS
        Label(self, justify=LEFT, wraplength=800, text=data[53+DATAOFFSET:54+DATAOFFSET].hex()).grid(row=25, column=6,sticky=W)

        #SAx_I
        Label(self, justify=LEFT, wraplength=800, text=data[55+DATAOFFSET:56+DATAOFFSET].hex()).grid(row=26, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[57+DATAOFFSET:58+DATAOFFSET].hex()).grid(row=26, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[59+DATAOFFSET:60+DATAOFFSET].hex()).grid(row=26, column=6,sticky=W)

        #CURRENT STATS
        Label(self, justify=LEFT, wraplength=800, text=data[61+DATAOFFSET:62+DATAOFFSET].hex()).grid(row=27, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[63+DATAOFFSET:64+DATAOFFSET].hex()).grid(row=27, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[65+DATAOFFSET:66+DATAOFFSET].hex()).grid(row=27, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[67+DATAOFFSET:68+DATAOFFSET].hex()).grid(row=27, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[69+DATAOFFSET:70+DATAOFFSET].hex()).grid(row=27, column=10,sticky=W)

        #SA TEMPS
        Label(self, justify=LEFT, wraplength=800, text=data[71+DATAOFFSET:72+DATAOFFSET].hex()).grid(row=28, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[73+DATAOFFSET:74+DATAOFFSET].hex()).grid(row=28, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[75+DATAOFFSET:76+DATAOFFSET].hex()).grid(row=28, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[77+DATAOFFSET:78+DATAOFFSET].hex()).grid(row=28, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[79+DATAOFFSET:80+DATAOFFSET].hex()).grid(row=28, column=10,sticky=W)

        #3V3EPS_I
        Label(self, justify=LEFT, wraplength=800, text=data[81+DATAOFFSET:82+DATAOFFSET].hex()).grid(row=29, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[83+DATAOFFSET:84+DATAOFFSET].hex()).grid(row=29, column=4,sticky=W)

        #HIST_SA_1
        Label(self, justify=LEFT, wraplength=800, text=data[85+DATAOFFSET:86+DATAOFFSET].hex()).grid(row=30, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[87+DATAOFFSET:88+DATAOFFSET].hex()).grid(row=30, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[89+DATAOFFSET:90+DATAOFFSET].hex()).grid(row=30, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[91+DATAOFFSET:92+DATAOFFSET].hex()).grid(row=30, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[93+DATAOFFSET:94+DATAOFFSET].hex()).grid(row=30, column=10,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[95+DATAOFFSET:96+DATAOFFSET].hex()).grid(row=30, column=12,sticky=W)

        #HIST_SA_2
        Label(self, justify=LEFT, wraplength=800, text=data[97+DATAOFFSET:98+DATAOFFSET].hex()).grid(row=31, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[99+DATAOFFSET:100+DATAOFFSET].hex()).grid(row=31, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[101+DATAOFFSET:102+DATAOFFSET].hex()).grid(row=31, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[103+DATAOFFSET:104+DATAOFFSET].hex()).grid(row=31, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[105+DATAOFFSET:106+DATAOFFSET].hex()).grid(row=31, column=10,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[107+DATAOFFSET:108+DATAOFFSET].hex()).grid(row=31, column=12,sticky=W)

        #HIST_SA_3
        Label(self, justify=LEFT, wraplength=800, text=data[109+DATAOFFSET:110+DATAOFFSET].hex()).grid(row=32, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[111+DATAOFFSET:112+DATAOFFSET].hex()).grid(row=32, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[113+DATAOFFSET:114+DATAOFFSET].hex()).grid(row=32, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[115+DATAOFFSET:116+DATAOFFSET].hex()).grid(row=32, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[117+DATAOFFSET:118+DATAOFFSET].hex()).grid(row=32, column=10,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[119+DATAOFFSET:120+DATAOFFSET].hex()).grid(row=32, column=12,sticky=W)

        #HIST_BATT_V
        Label(self, justify=LEFT, wraplength=800, text=data[121+DATAOFFSET:122+DATAOFFSET].hex()).grid(row=33, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[123+DATAOFFSET:124+DATAOFFSET].hex()).grid(row=33, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[125+DATAOFFSET:126+DATAOFFSET].hex()).grid(row=33, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[127+DATAOFFSET:128+DATAOFFSET].hex()).grid(row=33, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[129+DATAOFFSET:130+DATAOFFSET].hex()).grid(row=33, column=10,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[131+DATAOFFSET:132+DATAOFFSET].hex()).grid(row=33, column=12,sticky=W)

        #HIST_BATT_I
        Label(self, justify=LEFT, wraplength=800, text=data[133+DATAOFFSET:134+DATAOFFSET].hex()).grid(row=34, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[135+DATAOFFSET:136+DATAOFFSET].hex()).grid(row=34, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[137+DATAOFFSET:138+DATAOFFSET].hex()).grid(row=34, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[139+DATAOFFSET:140+DATAOFFSET].hex()).grid(row=34, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[141+DATAOFFSET:142+DATAOFFSET].hex()).grid(row=34, column=10,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=data[143+DATAOFFSET:144+DATAOFFSET].hex()).grid(row=34, column=12,sticky=W)



    def updateMisc(self,data):
        Label(self, justify=LEFT, wraplength=400, text=data.hex()).grid(row=100, column=2,sticky=W)


    def clock(self):
            self.timelabel = Label(self,height=3,bg="white", text=datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")).grid(row=1, column=2)                #goal is to update the clock constantly
            self.after(100,self.clock)



    def framcount(self):
    #will change this to represent the number of times that we have read data from the tcp port later
        DataGui.framcount += 1

    def threadedclock(self):


        updatetheclock = threading.Thread(target=self.clock)
        updatetheclock.isDaemon()
        updatetheclock.run()

    def lastpacketRecieved(self,data):
        Label(self, justify=LEFT, wraplength=800, text=data).grid(row=1, column=4,sticky=W)


class trackTCP(threading.Thread):
    def run(self):
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
                if(len(data) < 100 and len(data) > 75):
                    print("Tile data")
                    gui.updateTile(data)
                    gui.lastpacketRecieved(now)
                    print("{}".format(data))
                elif(len(data) < 213):
                    print("Health data")
                    gui.updateHealth(data)
                    gui.lastpacketRecieved(now)
                    print("{}".format(data))
                elif(len(data) > 213):
                    print("Power data")
                    gui.updatePower(data)
                    gui.updateMisc(data)
                    gui.lastpacketRecieved(now)
                    print("{}".format(data))
                else:
                    print("Miscellaneous data")
                    gui.updateMisc(data)
                    gui.lastpacketRecieved(now)
                    print("{}".format(data))


            except KeyboardInterrupt:
                print("should be exitiing")
                s.close()
                break


if __name__ == "__main__" :
    print("test")
    time = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")


    root = Tk()

    gui = DataGui(root)
    startup = 0

    test = trackTCP()
    test.start()
    gui.mainloop()

    #need to figure out how to update values on the run
