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

test_string_power = b'\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdb\xdc\x00\x00e\xb7\x00\x00\n\xe2\x00\xc5\x00\xc5\x00\x00\x00\x00\x00\x00\x00\x03\x00\xac\x00\x00\x00\x00\x03\xa7\x02o\x02\x18\x02\x14\x01\xc9\x01\xbf\x02p\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00>\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc4\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x0e\x01\x08\x01\x0c\x01\x08\x01\x0c\x01\x08\x02\x13\x02\x19\x02\x12\x02\x17\x02\x12\x02\x19\x81\xff\x82\x00\x81\xf8\x82\x00\x81\xff\x81\xf4S\xb6\xdb\xdc\xdb\xdc\xdb\xdc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0'

key_order = ['BYTES_SENT',
             'BYTES_RECIEVED',
             '',
             'PKTS_SENT',
             'PKTS_RECIEVED',
             '',
             'INVALID_PKTS_RECIEVED',
             'CRC_FAILS',
             '',
             'STATUS',
             'EPS_PIC_RESET_FLAGS',
             'EPS_WDT',
             '',
             'SA1_BOOST_V',
             'SA1_V',
             'SA1_I',
             '',
             'SA2_BOOST_V',
             'SA2_V',
             'SA2_I',
             '',
             'SA3_BOOST_V',
             'SA3_V',
             'SA3_I',
             '',
             'SA_Ym_TEMP',
             'SA_Zp_TEMP',
             'SA_Zm_TEMP',
             'SA_Xp_TEMP',
             'SA_Yp_TEMP',
             '',
             'VBATT_V',
             'CHARGE_I',
             'DISCHARGE_I',
             'BATT1_TEMP',
             'BATT2_TEMP',
             '',
             '5VBUS_V',
             '5VBUS_I',
             '5VBUS_TEMP',
             '',
             '33VBUS_V',
             '33VBUS_I',
             '33VBUS_TEMP',
             '',
             '33VEPS_V',
             '33VEPS_I',
             '',
             'VBATT1_V',
             'VBATT1_I',
             '',
             'VBATT2_V',
             'VBATT2_I']


Coeff = {}
Coeff['LARGE_V'] =      [0,         0.01368,            'V']
Coeff['STD_I'] =        [0,         1.611328125,        'mA']
Coeff['STD_V'] =        [0,         0.005317,           'V']
Coeff['AD590_TEMP'] =   [-273,      0.5462080078,       'C']
Coeff['SA_TEMP'] =      [-273,      0.7661,             'C']
Coeff['33EPS_I'] =      [0,         0.035413769,        'mA']
Coeff['HIST_SA_P'] =    [0,         0.00142185467128,   'W']
Coeff['BUS_TEMP'] =     [-238.85,   0.5776,             'C']
Coeff['BUS_I'] =        [10,        10,                 'mA']
Coeff['EPS_WDT'] =      [0,         0.0115833333333333, 'Hours']
Coeff['None'] =         [0,         1,                  '']






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


        Label(self, text="TILE DATA: ").grid(row=4, column=1,sticky=W)
        Label(self, text="S6 Count: ").grid(row=5, column=1,sticky=W)
        Label(self, text="ACT_TILES: ").grid(row=5, column=3,sticky=W)
        Label(self, text="FAULTED TILES: ").grid(row=5, column=5,sticky=W)
        Label(self, text="FAULTED COUNT1: ").grid(row=5, column=7,sticky=W)
        Label(self, text="FAULTED COUNT2: ").grid(row=5, column=9,sticky=W)

        Label(self, text="FAULTED COUNT3: ").grid(row=6, column=1,sticky=W)
        Label(self, text="FAULTED COUNT4: ").grid(row=6, column=3,sticky=W)
        Label(self, text="FAULTED COUNT5: ").grid(row=6, column=5,sticky=W)
        Label(self, text="FAULTED COUNT6: ").grid(row=6, column=7,sticky=W)
        Label(self, text="FAULTED COUNT7: ").grid(row=6, column=9,sticky=W)

        Label(self, text="FAULTED COUNT8: ").grid(row=7, column=1,sticky=W)
        Label(self, text="FAULTS INJECTED: ").grid(row=7, column=3,sticky=W)
        Label(self, text="TOTAL FAULTS  : ").grid(row=7, column=5,sticky=W)
        Label(self, text="MOVE_TILE_COUNT: ").grid(row=7, column=7,sticky=W)
        Label(self, text="NEXT_SPARE    : ").grid(row=7, column=9,sticky=W)

        Label(self, text="Readback Faults: ").grid(row=8, column=1,sticky=W)
        Label(self, text="Watchdog: ").grid(row=8, column=3,sticky=W)
        Label(self, text="ACT PROC1: ").grid(row=8, column=5,sticky=W)
        Label(self, text="ACT PROC2: ").grid(row=8, column=7,sticky=W)
        Label(self, text="ACT PROC3: ").grid(row=8, column=9,sticky=W)

        Label(self, text="ACTPROCCNT1: ").grid(row=9, column=1,sticky=W)
        Label(self, text="ACTPROCCNT2: ").grid(row=9, column=3,sticky=W)
        Label(self, text="ACTPROCCNT3: ").grid(row=9, column=5,sticky=W)
        Label(self, text="VOTER_COUNTS: ").grid(row=9, column=7,sticky=W)
        Label(self, text="CRC : ").grid(row=9, column=9,sticky=W)
        Label(self, text="SYNC: ").grid(row=9, column=11,sticky=W)



        #self.updateTile(test_string_tile)

        Frame(height=2, bg="black").grid(row=10,column=1,stick="nwes")

        Label(self, text="Health data: ").grid(row=11, column=1, sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=test_string_health.hex()).grid(row=11, column=2,sticky=W)
        Label(self, text=" ").grid(row=12, column=2,sticky=W)

        POWERROWOFFSET = 10
        Label(self, text="POWER DATA: ").grid(row=15+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="Bytes Sent: ").grid(row=16+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="Bytes Recv: ").grid(row=16+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="PKTS Sent: ").grid(row=17+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="PKTS Recv: ").grid(row=17+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="Invld Pack: ").grid(row=18+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="CRC  Fails: ").grid(row=18+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="status  : ").grid(row=19+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="Reset flag: ").grid(row=19+POWERROWOFFSET, column=3, sticky=W)

        Label(self, text="SA1_BOOST_V: ").grid( row=20+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="SA1_V: ").grid(row=20+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="SA2_BOOST_V: ").grid( row=21+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="SA2_V: ").grid(row=21+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="SA3_V: ").grid(row=22+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="SA3_BOOST_V: ").grid( row=22+POWERROWOFFSET, column=3, sticky=W)

        Label(self, text="BATT2_TEMP: ").grid(row=23+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="BATT1_TEMP: ").grid(row=23+POWERROWOFFSET, column=3, sticky=W)

        Label(self, text="5V0BUS_V: ").grid(row=23+POWERROWOFFSET, column=5, sticky=W)
        Label(self, text="3V3BUS_V: ").grid(row=23+POWERROWOFFSET, column=7, sticky=W)

        Label(self, text="VBATT2_V: ").grid(row=24+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="VBATT_V : ").grid(row=24+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="VBATT1_V: ").grid(row=24+POWERROWOFFSET, column=5, sticky=W)

        Label(self, text="3V3BUS_TEMP: ").grid(row=25+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="5V0BUS_TEMP: ").grid(row=25+POWERROWOFFSET, column=3, sticky=W)

        Label(self, text="3V3EPS_V   : ").grid(row=25+POWERROWOFFSET, column=5, sticky=W)

        Label(self, text="SA1_I: ").grid(row=26+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="SA2_I: ").grid(row=26+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="SA3_I: ").grid(row=26+POWERROWOFFSET, column=5, sticky=W)

        Label(self, text="DISCHARGE_I: ").grid(row=27+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="CHARGE_I   : ").grid(row=27+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="3V3BUS_I   : ").grid(row=27+POWERROWOFFSET, column=5, sticky=W)
        Label(self, text="VBATT1_I   : ").grid(row=27+POWERROWOFFSET, column=7, sticky=W)
        Label(self, text="VBATT2_I   : ").grid(row=27+POWERROWOFFSET, column=9, sticky=W)

        Label(self, text="SA_Ym_TEMP: ").grid(row=28+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="SA_Zp_TEMP: ").grid(row=28+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="SA_Zm_TEMP: ").grid(row=28+POWERROWOFFSET, column=5, sticky=W)
        Label(self, text="SA_Xp_TEMP: ").grid(row=28+POWERROWOFFSET, column=7, sticky=W)
        Label(self, text="SA_Yp_TEMP: ").grid(row=28+POWERROWOFFSET, column=9, sticky=W)

        Label(self, text="3V3EPS_I: ").grid(row=29+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="5V0BUS_I: ").grid(row=29+POWERROWOFFSET, column=3, sticky=W)

        Label(self, text="HIST_SA_1_P_1: ").grid(row=30+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="HIST_SA_1_P_2: ").grid(row=30+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="HIST_SA_1_P_3: ").grid(row=30+POWERROWOFFSET, column=5, sticky=W)
        Label(self, text="HIST_SA_1_P_4: ").grid(row=30+POWERROWOFFSET, column=7, sticky=W)
        Label(self, text="HIST_SA_1_P_5: ").grid(row=30+POWERROWOFFSET, column=9, sticky=W)
        Label(self, text="HIST_SA_1_P_6: ").grid(row=30+POWERROWOFFSET, column=11, sticky=W)

        Label(self, text="HIST_SA_2_P_1: ").grid(row=31+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="HIST_SA_2_P_2: ").grid(row=31+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="HIST_SA_2_P_3: ").grid(row=31+POWERROWOFFSET, column=5, sticky=W)
        Label(self, text="HIST_SA_2_P_4: ").grid(row=31+POWERROWOFFSET, column=7, sticky=W)
        Label(self, text="HIST_SA_2_P_5: ").grid(row=31+POWERROWOFFSET, column=9, sticky=W)
        Label(self, text="HIST_SA_2_P_6: ").grid(row=31+POWERROWOFFSET, column=11, sticky=W)

        Label(self, text="HIST_SA_3_P_1: ").grid(row=32+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="HIST_SA_3_P_2: ").grid(row=32+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="HIST_SA_3_P_3: ").grid(row=32+POWERROWOFFSET, column=5, sticky=W)
        Label(self, text="HIST_SA_3_P_4: ").grid(row=32+POWERROWOFFSET, column=7, sticky=W)
        Label(self, text="HIST_SA_3_P_5: ").grid(row=32+POWERROWOFFSET, column=9, sticky=W)
        Label(self, text="HIST_SA_3_P_6: ").grid(row=32+POWERROWOFFSET, column=11, sticky=W)

        Label(self, text="HIST_BATT_V_1: ").grid(row=33+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="HIST_BATT_V_2: ").grid(row=33+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="HIST_BATT_V_3: ").grid(row=33+POWERROWOFFSET, column=5, sticky=W)
        Label(self, text="HIST_BATT_V_4: ").grid(row=33+POWERROWOFFSET, column=7, sticky=W)
        Label(self, text="HIST_BATT_V_5: ").grid(row=33+POWERROWOFFSET, column=9, sticky=W)
        Label(self, text="HIST_BATT_V_6: ").grid(row=33+POWERROWOFFSET, column=11, sticky=W)

        Label(self, text="HIST_BATT_I_1: ").grid(row=34+POWERROWOFFSET, column=1, sticky=W)
        Label(self, text="HIST_BATT_I_2: ").grid(row=34+POWERROWOFFSET, column=3, sticky=W)
        Label(self, text="HIST_BATT_I_3: ").grid(row=34+POWERROWOFFSET, column=5, sticky=W)
        Label(self, text="HIST_BATT_I_4: ").grid(row=34+POWERROWOFFSET, column=7, sticky=W)
        Label(self, text="HIST_BATT_I_5: ").grid(row=34+POWERROWOFFSET, column=9, sticky=W)
        Label(self, text="HIST_BATT_I_6: ").grid(row=34+POWERROWOFFSET, column=11, sticky=W)

        #self.updatePower(test_string_health)

        Label(self, text="Misc data/Powerchunk: ").grid(row=100, column=1, sticky=W)


    def updateTile(self,data):
        OFFSET = 18
        Label(self, justify=LEFT, wraplength=400, text=data[0+OFFSET:3+OFFSET].hex()).grid(row=5, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[3+OFFSET:5+OFFSET].hex()).grid(row=5, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[5+OFFSET:7+OFFSET].hex()).grid(row=5, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[7+OFFSET:9+OFFSET].hex()).grid(row=5, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[9+OFFSET:11+OFFSET].hex()).grid(row=5, column=10,sticky=W)

        Label(self, justify=LEFT, wraplength=400, text=data[11+OFFSET:13+OFFSET].hex()).grid(row=6, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[13+OFFSET:15+OFFSET].hex()).grid(row=6, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[15+OFFSET:17+OFFSET].hex()).grid(row=6, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[17+OFFSET:19+OFFSET].hex()).grid(row=6, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[19+OFFSET:21+OFFSET].hex()).grid(row=6, column=10,sticky=W)

        Label(self, justify=LEFT, wraplength=400, text=data[23+OFFSET:25+OFFSET].hex()).grid(row=7, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[25+OFFSET:27+OFFSET].hex()).grid(row=7, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[27+OFFSET:29+OFFSET].hex()).grid(row=7, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[29+OFFSET:31+OFFSET].hex()).grid(row=7, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[31+OFFSET:32+OFFSET].hex()).grid(row=7, column=10,sticky=W)

        Label(self, justify=LEFT, wraplength=400, text=data[33+OFFSET:34+OFFSET].hex()).grid(row=8, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[34+OFFSET:35+OFFSET].hex()).grid(row=8, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[35+OFFSET:36+OFFSET].hex()).grid(row=8, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[36+OFFSET:37+OFFSET].hex()).grid(row=8, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[37+OFFSET:38+OFFSET].hex()).grid(row=8, column=10,sticky=W)

        Label(self, justify=LEFT, wraplength=400, text=data[38+OFFSET:40+OFFSET].hex()).grid(row=9, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[40+OFFSET:42+OFFSET].hex()).grid(row=9, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[42+OFFSET:44+OFFSET].hex()).grid(row=9, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[44+OFFSET:46+OFFSET].hex()).grid(row=9, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[46+OFFSET:48+OFFSET].hex()).grid(row=9, column=10,sticky=W)
        Label(self, justify=LEFT, wraplength=400, text=data[48+OFFSET:49+OFFSET].hex()).grid(row=9, column=12,sticky=W)




    def updateHealth(self,data):
        Label(self, justify=LEFT, wraplength=400, text=data.hex()).grid(row=11, column=2,sticky=W)

    def updatePower(self,data):
        DATAOFFSET = 32
        POWERROWOFFSET = 10

        #Initial set of data from EPS
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[0+DATAOFFSET:4+DATAOFFSET].hex(),16))).grid(row=16+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[4+DATAOFFSET:8+DATAOFFSET].hex(),16))).grid(row=16+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[8+DATAOFFSET:10+DATAOFFSET].hex(),16))).grid(row=17+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[10+DATAOFFSET:12+DATAOFFSET].hex(),16))).grid(row=17+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[12+DATAOFFSET:14+DATAOFFSET].hex(),16))).grid(row=18+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[14+DATAOFFSET:16+DATAOFFSET].hex(),16))).grid(row=18+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[16+DATAOFFSET:18+DATAOFFSET].hex(),16))).grid(row=19+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[18+DATAOFFSET:20+DATAOFFSET].hex(),16))).grid(row=19+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[20+DATAOFFSET:22+DATAOFFSET].hex(),16))).grid(row=20+POWERROWOFFSET, column=2,sticky=W)

        #SA1 SA2 SA3
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[22+DATAOFFSET:24+DATAOFFSET].hex(),16))).grid(row=20+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[24+DATAOFFSET:26+DATAOFFSET].hex(),16))).grid(row=20+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[26+DATAOFFSET:28+DATAOFFSET].hex(),16))).grid(row=21+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[28+DATAOFFSET:30+DATAOFFSET].hex(),16))).grid(row=21+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[30+DATAOFFSET:32+DATAOFFSET].hex(),16))).grid(row=22+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[32+DATAOFFSET:34+DATAOFFSET].hex(),16))).grid(row=22+POWERROWOFFSET, column=4,sticky=W)

        #BATT TEMPS
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[34+DATAOFFSET:36+DATAOFFSET].hex(),16))).grid(row=23+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[36+DATAOFFSET:38+DATAOFFSET].hex(),16))).grid(row=23+POWERROWOFFSET, column=4,sticky=W)

        #BUS VOLTAGE
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[38+DATAOFFSET:40+DATAOFFSET].hex(),16))).grid(row=23+POWERROWOFFSET, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[40+DATAOFFSET:42+DATAOFFSET].hex(),16))).grid(row=23+POWERROWOFFSET, column=8,sticky=W)

        #BATTERY VOLTAGE
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[42+DATAOFFSET:44+DATAOFFSET].hex(),16))).grid(row=24+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[44+DATAOFFSET:46+DATAOFFSET].hex(),16))).grid(row=24+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[46+DATAOFFSET:48+DATAOFFSET].hex(),16))).grid(row=24+POWERROWOFFSET, column=6,sticky=W)

        #BUS TEMPS
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[48+DATAOFFSET:50+DATAOFFSET].hex(),16))).grid(row=25+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[50+DATAOFFSET:52+DATAOFFSET].hex(),16))).grid(row=25+POWERROWOFFSET, column=4,sticky=W)

        #3V3EPS
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[52+DATAOFFSET:54+DATAOFFSET].hex(),16))).grid(row=25+POWERROWOFFSET, column=6,sticky=W)

        #SAx_I
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[54+DATAOFFSET:56+DATAOFFSET].hex(),16))).grid(row=26+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[56+DATAOFFSET:58+DATAOFFSET].hex(),16))).grid(row=26+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[58+DATAOFFSET:60+DATAOFFSET].hex(),16))).grid(row=26+POWERROWOFFSET, column=6,sticky=W)

        #CURRENT STATS
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[60+DATAOFFSET:62+DATAOFFSET].hex(),16))).grid(row=27+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[62+DATAOFFSET:64+DATAOFFSET].hex(),16))).grid(row=27+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[64+DATAOFFSET:66+DATAOFFSET].hex(),16))).grid(row=27+POWERROWOFFSET, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[66+DATAOFFSET:68+DATAOFFSET].hex(),16))).grid(row=27+POWERROWOFFSET, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[68+DATAOFFSET:70+DATAOFFSET].hex(),16))).grid(row=27+POWERROWOFFSET, column=10,sticky=W)

        #SA TEMPS
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[70+DATAOFFSET:72+DATAOFFSET].hex(),16))).grid(row=28+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[72+DATAOFFSET:74+DATAOFFSET].hex(),16))).grid(row=28+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[74+DATAOFFSET:76+DATAOFFSET].hex(),16))).grid(row=28+POWERROWOFFSET, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[76+DATAOFFSET:78+DATAOFFSET].hex(),16))).grid(row=28+POWERROWOFFSET, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[78+DATAOFFSET:80+DATAOFFSET].hex(),16))).grid(row=28+POWERROWOFFSET, column=10,sticky=W)

        #3V3EPS_I
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[80+DATAOFFSET:82+DATAOFFSET].hex(),16))).grid(row=29+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[82+DATAOFFSET:84+DATAOFFSET].hex(),16))).grid(row=29+POWERROWOFFSET, column=4,sticky=W)

        #HIST_SA_1
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[84+DATAOFFSET:86+DATAOFFSET].hex(),16))).grid(row=30+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[86+DATAOFFSET:88+DATAOFFSET].hex(),16))).grid(row=30+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[88+DATAOFFSET:90+DATAOFFSET].hex(),16))).grid(row=30+POWERROWOFFSET, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[90+DATAOFFSET:92+DATAOFFSET].hex(),16))).grid(row=30+POWERROWOFFSET, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[92+DATAOFFSET:94+DATAOFFSET].hex(),16))).grid(row=30+POWERROWOFFSET, column=10,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[94+DATAOFFSET:96+DATAOFFSET].hex(),16))).grid(row=30+POWERROWOFFSET, column=12,sticky=W)

        #HIST_SA_2
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[96+DATAOFFSET:98+DATAOFFSET].hex(),16))).grid(row=31+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[98+DATAOFFSET:100+DATAOFFSET].hex(),16))).grid(row=31+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[100+DATAOFFSET:102+DATAOFFSET].hex(),16))).grid(row=31+POWERROWOFFSET, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[102+DATAOFFSET:104+DATAOFFSET].hex(),16))).grid(row=31+POWERROWOFFSET, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[104+DATAOFFSET:106+DATAOFFSET].hex(),16))).grid(row=31+POWERROWOFFSET, column=10,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[106+DATAOFFSET:108+DATAOFFSET].hex(),16))).grid(row=31+POWERROWOFFSET, column=12,sticky=W)

        #HIST_SA_3
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[108+DATAOFFSET:110+DATAOFFSET].hex(),16))).grid(row=32+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[110+DATAOFFSET:112+DATAOFFSET].hex(),16))).grid(row=32+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[112+DATAOFFSET:114+DATAOFFSET].hex(),16))).grid(row=32+POWERROWOFFSET, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[114+DATAOFFSET:116+DATAOFFSET].hex(),16))).grid(row=32+POWERROWOFFSET, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[116+DATAOFFSET:118+DATAOFFSET].hex(),16))).grid(row=32+POWERROWOFFSET, column=10,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[118+DATAOFFSET:120+DATAOFFSET].hex(),16))).grid(row=32+POWERROWOFFSET, column=12,sticky=W)

        #HIST_BATT_V
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[120+DATAOFFSET:122+DATAOFFSET].hex(),16))).grid(row=33+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[122+DATAOFFSET:124+DATAOFFSET].hex(),16))).grid(row=33+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[124+DATAOFFSET:126+DATAOFFSET].hex(),16))).grid(row=33+POWERROWOFFSET, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[126+DATAOFFSET:128+DATAOFFSET].hex(),16))).grid(row=33+POWERROWOFFSET, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[128+DATAOFFSET:130+DATAOFFSET].hex(),16))).grid(row=33+POWERROWOFFSET, column=10,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[130+DATAOFFSET:132+DATAOFFSET].hex(),16))).grid(row=33+POWERROWOFFSET, column=12,sticky=W)

        #HIST_BATT_I
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[132+DATAOFFSET:134+DATAOFFSET].hex(),16))).grid(row=34+POWERROWOFFSET, column=2,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[134+DATAOFFSET:136+DATAOFFSET].hex(),16))).grid(row=34+POWERROWOFFSET, column=4,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[136+DATAOFFSET:138+DATAOFFSET].hex(),16))).grid(row=34+POWERROWOFFSET, column=6,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[138+DATAOFFSET:140+DATAOFFSET].hex(),16))).grid(row=34+POWERROWOFFSET, column=8,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[140+DATAOFFSET:142+DATAOFFSET].hex(),16))).grid(row=34+POWERROWOFFSET, column=10,sticky=W)
        Label(self, justify=LEFT, wraplength=800, text=str(int(data[142+DATAOFFSET:144+DATAOFFSET].hex(),16))).grid(row=34+POWERROWOFFSET, column=12,sticky=W)



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
                    print("{}".format(data.hex()))
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
