#   Author: Skylar Tamke
#   with help from:  Johnny Gaddis
#
#
#

import sys
import socket
import serial
import logging
import datetime
import threading
from tkinter import *
from time import sleep

test_string_health = b'\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x13\x00\x00\x00{\xdc3\x1d\x10\x1dB\x1d\x9e\x00\x00\x0c\xea\x0c\xe2\x0c\xea\x0c\xd7\t\xc1\t\xca\t\xd6\t\xbf\x07\x07\x07\x07\x07\x0c\x06\xfa\x03\xe1\x03\xe7\x03\xf1\x03\xda\x03\xb5\x03\xb6\x03\xbb\x03\xb2\t\xc4\t\xa7\n`\x00\x00\x02q\x02q\x02q\x02q\x07\xef\x08r\t\xc4\x07S\x04\xe2\x04\x86\x04\xe2\x04E\x06\xb6\x05\xcd\x06\xb6\x04\xe2\x08\x8b\x08\x8b\x08\x8b\x08\x8b}\xfajR\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x1b\x00\x00\x00%\xcc\xcc\xdc'

test_string_tile = b'\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00J\xdc\x88\x00\x00\xd7\xe8\x02\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xf8\x03\x00\x00\x00\x00\x00\x00\x07\xeb\x07\xeb\x07\xeb\x00\x03\xcc\xcc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdc\x00\x00\x00\x00\x00\x00\xc0'

test_string_power = b'\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\xdb\xdc\x00\x00e\xb7\x00\x00\n\xe2\x00\xc5\x00\xc5\x00\x00\x00\x00\x00\x00\x00\x03\x00\xac\x00\x00\x00\x00\x03\xa7\x02o\x02\x18\x02\x14\x01\xc9\x01\xbf\x02p\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00>\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc4\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x0e\x01\x08\x01\x0c\x01\x08\x01\x0c\x01\x08\x02\x13\x02\x19\x02\x12\x02\x17\x02\x12\x02\x19\x81\xff\x82\x00\x81\xf8\x82\x00\x81\xff\x81\xf4S\xb6\xdb\xdc\xdb\xdc\xdb\xdc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0'


USB = serial.Serial("COM4", 115200)

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
Coeff['LARGE_V'] =	  [0,		 0.01368,			'V']
Coeff['STD_I'] =		[0,		 1.611328125,		'mA']
Coeff['STD_V'] =		[0,		 0.005317,		   'V']
Coeff['AD590_TEMP'] =   [-273,	  0.5462080078,	   'C']
Coeff['SA_TEMP'] =	  [-273,	  0.7661,			 'C']
Coeff['33EPS_I'] =	  [0,		 0.035413769,		'mA']
Coeff['HIST_SA_P'] =	[0,		 0.00142185467128,   'W']
Coeff['BUS_TEMP'] =	 [-238.85,   0.5776,			 'C']
Coeff['BUS_I'] =		[10,		10,				 'mA']
Coeff['EPS_WDT'] =	  [0,		 0.0115833333333333, 'Hours']
Coeff['None'] =		 [0,		 1,				  '']






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


		self.TILE_DATA = Label(self, text="TILE DATA: ")
		self.TILE_DATA.grid(row=4, column=1,sticky=W)
		self.S6_COUNT = Label(self, text="S6 Count: ")
		self.S6_COUNT.grid(row=5, column=1,sticky=W)
		self.ACT_TILES = Label(self, text="ACT_TILES: ")
		self.ACT_TILES.grid(row=5, column=3,sticky=W)
		self.FAULTED_TILES = Label(self, text="FAULTED TILES: ")
		self.FAULTED_TILES.grid(row=5, column=5,sticky=W)
		self.FAULTED_COUNT1 = Label(self, text="FAULTED COUNT1: ")
		self.FAULTED_COUNT1.grid(row=5, column=7,sticky=W)
		self.FAULTED_COUNT2 = Label(self, text="FAULTED COUNT2: ")
		self.FAULTED_COUNT2.grid(row=5, column=9,sticky=W)
		self.FAULTED_COUNT3 = Label(self, text="FAULTED COUNT3: ")
		self.FAULTED_COUNT3.grid(row=6, column=1,sticky=W)
		self.FAULTED_COUNT4 = Label(self, text="FAULTED COUNT4: ")
		self.FAULTED_COUNT4.grid(row=6, column=3,sticky=W)
		self.FAULTED_COUNT5 = Label(self, text="FAULTED COUNT5: ")
		self.FAULTED_COUNT5.grid(row=6, column=5,sticky=W)
		self.FAULTED_COUNT6 = Label(self, text="FAULTED COUNT6: ")
		self.FAULTED_COUNT6.grid(row=6, column=7,sticky=W)
		self.FAULTED_COUNT7 = Label(self, text="FAULTED COUNT7: ")
		self.FAULTED_COUNT7.grid(row=6, column=9,sticky=W)

		self.FAULTED_COUNT8 = Label(self, text="FAULTED COUNT8: ")
		self.FAULTED_COUNT8.grid(row=7, column=1,sticky=W)
		self.FAULTS_INJECTED = Label(self, text="FAULTS INJECTED: ")
		self.FAULTS_INJECTED.grid(row=7, column=3,sticky=W)
		self.TOTAL_FAULTS = Label(self, text="TOTAL FAULTS  : ")
		self.TOTAL_FAULTS.grid(row=7, column=5,sticky=W)
		self.MOVE_TILE_COUNT = Label(self, text="MOVE_TILE_COUNT: ")
		self.MOVE_TILE_COUNT.grid(row=7, column=7,sticky=W)
		self.NEXT_SPARE = Label(self, text="NEXT_SPARE: ")
		self.NEXT_SPARE.grid(row=7, column=9,sticky=W)

		self.READBACK_FAULTS = Label(self, text="Readback Faults: ")
		self.READBACK_FAULTS.grid(row=8, column=1,sticky=W)
		self.WATCHDOG = Label(self, text="Watchdog: ")
		self.WATCHDOG.grid(row=8, column=3,sticky=W)
		self.ACT_PROC1 = Label(self, text="ACT PROC1: ")
		self.ACT_PROC1.grid(row=8, column=5,sticky=W)
		self.ACT_PROC2 = Label(self, text="ACT PROC2: ")
		self.ACT_PROC2.grid(row=8, column=7,sticky=W)
		self.ACT_PROC3 = Label(self, text="ACT PROC3: ")
		self.ACT_PROC3.grid(row=8, column=9,sticky=W)

		self.ACTPROCCNT1 = Label(self, text="ACTPROCCNT1: ")
		self.ACTPROCCNT1.grid(row=9, column=1,sticky=W)
		self.ACTPROCCNT2 = Label(self, text="ACTPROCCNT2: ")
		self.ACTPROCCNT2.grid(row=9, column=3,sticky=W)
		self.ACTPROCCNT3 = Label(self, text="ACTPROCCNT3: ")
		self.ACTPROCCNT3.grid(row=9, column=5,sticky=W)
		self.VOTER_COUNTS = Label(self, text="VOTER_COUNTS: ")
		self.VOTER_COUNTS.grid(row=9, column=7,sticky=W)
		self.CRC_TILE = Label(self, text="CRC : ")
		self.CRC_TILE.grid(row=9, column=9,sticky=W)
		self.SYNC = Label(self, text="SYNC: ")
		self.SYNC.grid(row=9, column=11,sticky=W)


		#self.updateTile(test_string_tile)
		Frame(height=2, bg="black").grid(row=10,column=1,stick="nwes")

		Label(self, text="HEALTH DATA: ").grid(row=11, column=1, sticky=W)
		#self. = Label(self, text="PKT TYPE: ").grid(row=12, column=1, sticky=W)

		### VOLTAGE ###
		self.VOLTAGE_INS_IN = Label(self, text="VOLTAGE_INS_IN: ")
		self.VOLTAGE_INS_IN.grid(row=13, column=1, sticky=W)
		self.VOLTAGE_AVE_IN = Label(self, text="VOLTAGE_AVE_IN: ")
		self.VOLTAGE_AVE_IN.grid(row=14, column=1, sticky=W)
		self.VOLTAGE_MAX_IN = Label(self, text="VOLTAGE_MAX_IN: ")
		self.VOLTAGE_MAX_IN.grid(row=15, column=1, sticky=W)
		self.VOLTAGE_MIN_IN = Label(self, text="VOLTAGE_MIN_IN: ")
		self.VOLTAGE_MIN_IN.grid(row=16, column=1, sticky=W)
		self.VOLTAGE_INS_3V3D = Label(self, text="VOLTAGE_INS_3V3D: ")
		self.VOLTAGE_INS_3V3D.grid(row=17, column=1, sticky=W)
		self.VOLTAGE_AVE_3V3D = Label(self, text="VOLTAGE_AVE_3V3D: ")
		self.VOLTAGE_AVE_3V3D.grid(row=18, column=1, sticky=W)
		self.VOLTAGE_MAX_3V3D = Label(self, text="VOLTAGE_MAX_3V3D: ")
		self.VOLTAGE_MAX_3V3D.grid(row=19, column=1, sticky=W)
		self.VOLTAGE_MIN_3V3D = Label(self, text="VOLTAGE_MIN_3V3D: ")
		self.VOLTAGE_MIN_3V3D.grid(row=20, column=1, sticky=W)
		self.VOLTAGE_INS_2V5D = Label(self, text="VOLTAGE_INS_2V5D: ")
		self.VOLTAGE_INS_2V5D.grid(row=13, column=3, sticky=W)
		self.VOLTAGE_AVE_2V5D = Label(self, text="VOLTAGE_AVE_2V5D: ")
		self.VOLTAGE_AVE_2V5D.grid(row=14, column=3, sticky=W)
		self.VOLTAGE_MAX_2V5D = Label(self, text="VOLTAGE_MAX_2V5D: ")
		self.VOLTAGE_MAX_2V5D.grid(row=15, column=3, sticky=W)
		self.VOLTAGE_MIN_2V5D = Label(self, text="VOLTAGE_MIN_2V5D: ")
		self.VOLTAGE_MIN_2V5D.grid(row=16, column=3, sticky=W)
		self.VOLTAGE_INS_1V8D = Label(self, text="VOLTAGE_INS_1V8D: ")
		self.VOLTAGE_INS_1V8D.grid(row=17, column=3, sticky=W)
		self.VOLTAGE_AVE_1V8D = Label(self, text="VOLTAGE_AVE_1V8D: ")
		self.VOLTAGE_AVE_1V8D.grid(row=18, column=3, sticky=W)
		self.VOLTAGE_MAX_1V8D = Label(self, text="VOLTAGE_MAX_1V8D: ")
		self.VOLTAGE_MAX_1V8D.grid(row=19, column=3, sticky=W)
		self.VOLTAGE_MIN_1V8D = Label(self, text="VOLTAGE_MIN_1V8D: ")
		self.VOLTAGE_MIN_1V8D.grid(row=20, column=3, sticky=W)
		self.VOLTAGE_INS_1V0SD = Label(self, text="VOLTAGE_INS_1V0SD: ")
		self.VOLTAGE_INS_1V0SD.grid(row=13, column=5, sticky=W)
		self.VOLTAGE_AVE_1V0SD = Label(self, text="VOLTAGE_AVE_1V0SD: ")
		self.VOLTAGE_AVE_1V0SD.grid(row=14, column=5, sticky=W)
		self.VOLTAGE_MAX_1V0SD = Label(self, text="VOLTAGE_MAX_1V0SD: ")
		self.VOLTAGE_MAX_1V0SD.grid(row=15, column=5, sticky=W)
		self.VOLTAGE_MIN_1V0SD = Label(self, text="VOLTAGE_MIN_1V0SD: ")
		self.VOLTAGE_MIN_1V0SD.grid(row=16, column=5, sticky=W)
		self.VOLTAGE_INS_0V95AD = Label(self, text="VOLTAGE_INS_0V95AD: ")
		self.VOLTAGE_INS_0V95AD.grid(row=17, column=5, sticky=W)
		self.VOLTAGE_AVE_0V95AD = Label(self, text="VOLTAGE_AVE_0V95AD: ")
		self.VOLTAGE_AVE_0V95AD.grid(row=18, column=5, sticky=W)
		self.VOLTAGE_MAX_0V95AD = Label(self, text="VOLTAGE_MAX_0V95AD: ")
		self.VOLTAGE_MAX_0V95AD.grid(row=19, column=5, sticky=W)
		self.VOLTAGE_MIN_0V95AD = Label(self, text="VOLTAGE_MIN_0V95AD: ")
		self.VOLTAGE_MIN_0V95AD.grid(row=20, column=5, sticky=W)

		### CURRENTS ###
		self.CURRENT_INS_IN = Label(self, text="CURRENT_INS_IN: ")
		self.CURRENT_INS_IN.grid(row=13, column=   7, sticky=W)
		self.CURRENT_AVE_IN = Label(self, text="CURRENT_AVE_IN: ")
		self.CURRENT_AVE_IN.grid(row=14, column=   7, sticky=W)
		self.CURRENT_MAX_IN = Label(self, text="CURRENT_MAX_IN: ")
		self.CURRENT_MAX_IN.grid(row=15, column=   7, sticky=W)
		self.CURRENT_MIN_IN = Label(self, text="CURRENT_MIN_IN: ")
		self.CURRENT_MIN_IN.grid(row=16, column=   7, sticky=W)
		self.CURRENT_INS_3V3D = Label(self, text="CURRENT_INS_3V3D: ")
		self.CURRENT_INS_3V3D.grid(row=17, column= 7, sticky=W)
		self.CURRENT_AVE_3V3D = Label(self, text="CURRENT_AVE_3V3D: ")
		self.CURRENT_AVE_3V3D.grid(row=18, column= 7, sticky=W)
		self.CURRENT_MAX_3V3D = Label(self, text="CURRENT_MAX_3V3D: ")
		self.CURRENT_MAX_3V3D.grid(row=19, column= 7, sticky=W)
		self.CURRENT_MIN_3V3D = Label(self, text="CURRENT_MIN_3V3D: ")
		self.CURRENT_MIN_3V3D.grid(row=20, column= 7, sticky=W)
		self.CURRENT_INS_2V5D = Label(self, text="CURRENT_INS_2V5D: ")
		self.CURRENT_INS_2V5D.grid(row=13, column= 9, sticky=W)
		self.CURRENT_AVE_2V5D = Label(self, text="CURRENT_AVE_2V5D: ")
		self.CURRENT_AVE_2V5D.grid(row=14, column= 9, sticky=W)
		self.CURRENT_MAX_2V5D = Label(self, text="CURRENT_MAX_2V5D: ")
		self.CURRENT_MAX_2V5D.grid(row=15, column= 9, sticky=W)
		self.CURRENT_MIN_2V5D = Label(self, text="CURRENT_MIN_2V5D: ")
		self.CURRENT_MIN_2V5D.grid(row=16, column= 9, sticky=W)
		self.CURRENT_INS_1V8D = Label(self, text="CURRENT_INS_1V8D: ")
		self.CURRENT_INS_1V8D.grid(row=17, column= 9, sticky=W)
		self.CURRENT_AVE_1V8D = Label(self, text="CURRENT_AVE_1V8D: ")
		self.CURRENT_AVE_1V8D.grid(row=18, column= 9, sticky=W)
		self.CURRENT_MAX_1V8D = Label(self, text="CURRENT_MAX_1V8D: ")
		self.CURRENT_MAX_1V8D.grid(row=19, column= 9, sticky=W)
		self.CURRENT_MIN_1V8D = Label(self, text="CURRENT_MIN_1V8D: ")
		self.CURRENT_MIN_1V8D.grid(row=20, column= 9, sticky=W)
		self.CURRENT_INS_1V0SD = Label(self, text="CURRENT_INS_1V0SD: ")
		self.CURRENT_INS_1V0SD.grid(row=13, column= 11, sticky=W)
		self.CURRENT_AVE_1V0SD = Label(self, text="CURRENT_AVE_1V0SD: ")
		self.CURRENT_AVE_1V0SD.grid(row=14, column= 11, sticky=W)
		self.CURRENT_MAX_1V0SD = Label(self, text="CURRENT_MAX_1V0SD: ")
		self.CURRENT_MAX_1V0SD.grid(row=15, column= 11, sticky=W)
		self.CURRENT_MIN_1V0SD = Label(self, text="CURRENT_MIN_1V0SD: ")
		self.CURRENT_MIN_1V0SD.grid(row=16, column= 11, sticky=W)
		self.CURRENT_INS_0V95AD = Label(self, text="CURRENT_INS_0V95AD: ")
		self.CURRENT_INS_0V95AD.grid(row=17, column=11, sticky=W)
		self.CURRENT_AVE_0V95AD = Label(self, text="CURRENT_AVE_0V95AD: ")
		self.CURRENT_AVE_0V95AD.grid(row=18, column=11, sticky=W)
		self.CURRENT_MAX_0V95AD = Label(self, text="CURRENT_MAX_0V95AD: ")
		self.CURRENT_MAX_0V95AD.grid(row=19, column=11, sticky=W)
		self.CURRENT_MIN_0V95AD = Label(self, text="CURRENT_MIN_0V95AD: ")
		self.CURRENT_MIN_0V95AD.grid(row=20, column=11, sticky=W)

		self.A7_TEMPERATURE = Label(self, text="A7_TEMPERATURE: ")
		self.A7_TEMPERATURE.grid(row=13, column=13, stick=W)
		self.PC1_TEMPERATURE = Label(self, text="PC1_TEMPERATURE: ")
		self.PC1_TEMPERATURE.grid(row=14, column=13, stick=W)
		self.PC2_TEMPERATURE = Label(self, text="PC2_TEMPERATURE: ")
		self.PC2_TEMPERATURE.grid(row=15, column=13, stick=W)

		self.DAYS = Label(self, text="DAYS: ")
		self.DAYS.grid(row=16, column=   13, sticky=W)
		self.HOURS = Label(self, text="HOURS: ")
		self.HOURS.grid(row=17, column=  13, sticky=W)
		self.MINUTES = Label(self, text="MINUTES: ")
		self.MINUTES.grid(row=18, column=13, sticky=W)
		self.SECONDS = Label(self, text="SECONDS: ")
		self.SECONDS.grid(row=19, column=13, sticky=W)
		self.CRC_HEALTH = Label(self, text="CRC: ")
		self.CRC_HEALTH.grid(row=20, column=13, sticky=W)
		# Label(self, justify=LEFT, wraplength=400, text=test_string_health.hex()).grid(row=11, column=2,sticky=W)
		# Label(self, text=" ").grid(row=12, column=2,sticky=W)

		POWERROWOFFSET = 10

		self.POWER_DATA = Label(self, text=" ")
		self.POWER_DATA.grid(row=14+POWERROWOFFSET, column=1, sticky=W)

		self.POWER_DATA = Label(self, text="POWER DATA: ")
		self.POWER_DATA.grid(row=15+POWERROWOFFSET, column=1, sticky=W)
		self.BYTES_SENT = Label(self, text="Bytes Sent: ")
		self.BYTES_SENT.grid(row=16+POWERROWOFFSET, column=1, sticky=W)
		self.BYTES_RECV = Label(self, text="Bytes Recv: ")
		self.BYTES_RECV.grid(row=16+POWERROWOFFSET, column=3, sticky=W)
		self.PKTS_SENT = Label(self, text="PKTS Sent: ")
		self.PKTS_SENT.grid(row=17+POWERROWOFFSET, column=1, sticky=W)
		self.PKTS_RECV = Label(self, text="PKTS Recv: ")
		self.PKTS_RECV.grid(row=17+POWERROWOFFSET, column=3, sticky=W)
		self.INVLD_PACK = Label(self, text="Invld Pack: ")
		self.INVLD_PACK.grid(row=18+POWERROWOFFSET, column=1, sticky=W)
		self.CRC_FAILS = Label(self, text="CRC  Fails: ")
		self.CRC_FAILS.grid(row=18+POWERROWOFFSET, column=3, sticky=W)
		self.STATUS = Label(self, text="status  : ")
		self.STATUS.grid(row=19+POWERROWOFFSET, column=1, sticky=W)
		self.RESET_FLAG = Label(self, text="Reset flag: ")
		self.RESET_FLAG.grid(row=19+POWERROWOFFSET, column=3, sticky=W)
		POWERROWOFFSET = 10
		self.SA1_BOOST_V = Label(self, text="SA1_BOOST_V: ")
		self.SA1_BOOST_V.grid( row=20+POWERROWOFFSET, column=1, sticky=W)
		self.SA1_V = Label(self, text="SA1_V: ")
		self.SA1_V.grid(row=20+POWERROWOFFSET, column=3, sticky=W)
		self.SA2_BOOST_V = Label(self, text="SA2_BOOST_V: ")
		self.SA2_BOOST_V.grid( row=21+POWERROWOFFSET, column=1, sticky=W)
		self.SA2_V = Label(self, text="SA2_V: ")
		self.SA2_V.grid(row=21+POWERROWOFFSET, column=3, sticky=W)
		self.SA3_V = Label(self, text="SA3_V: ")
		self.SA3_V.grid(row=22+POWERROWOFFSET, column=1, sticky=W)
		self.SA3_BOOST_V = Label(self, text="SA3_BOOST_V: ")
		self.SA3_BOOST_V.grid( row=22+POWERROWOFFSET, column=3, sticky=W)

		self.BATT2_TEMP = Label(self, text="BATT2_TEMP: ")
		self.BATT2_TEMP.grid(row=23+POWERROWOFFSET, column=1, sticky=W)
		self.BATT1_TEMP = Label(self, text="BATT1_TEMP: ")
		self.BATT1_TEMP.grid(row=23+POWERROWOFFSET, column=3, sticky=W)

		self.FIVEV0BUS_V = Label(self, text="5V0BUS_V: ")
		self.FIVEV0BUS_V.grid(row=23+POWERROWOFFSET, column=5, sticky=W)
		self.THREEV3BUS_V = Label(self, text="3V3BUS_V: ")
		self.THREEV3BUS_V.grid(row=23+POWERROWOFFSET, column=7, sticky=W)

		self.VBATT2_V = Label(self, text="VBATT2_V: ")
		self.VBATT2_V.grid(row=24+POWERROWOFFSET, column=1, sticky=W)
		self.VBATT_V = Label(self, text="VBATT_V : ")
		self.VBATT_V.grid(row=24+POWERROWOFFSET, column=3, sticky=W)
		self.VBATT1_V = Label(self, text="VBATT1_V: ")
		self.VBATT1_V.grid(row=24+POWERROWOFFSET, column=5, sticky=W)

		self.THREEV3BUS_TEMP = Label(self, text="3V3BUS_TEMP: ")
		self.THREEV3BUS_TEMP.grid(row=25+POWERROWOFFSET, column=1, sticky=W)
		self.FIVEV0BUS_TEMP = Label(self, text="5V0BUS_TEMP: ")
		self.FIVEV0BUS_TEMP.grid(row=25+POWERROWOFFSET, column=3, sticky=W)

		self.THREEV3EPS_V = Label(self, text="3V3EPS_V   : ")
		self.THREEV3EPS_V.grid(row=25+POWERROWOFFSET, column=5, sticky=W)

		self.SA1_I = Label(self, text="SA1_I: ")
		self.SA1_I.grid(row=26+POWERROWOFFSET, column=1, sticky=W)
		self.SA2_I = Label(self, text="SA2_I: ")
		self.SA2_I.grid(row=26+POWERROWOFFSET, column=3, sticky=W)
		self.SA3_I = Label(self, text="SA3_I: ")
		self.SA3_I.grid(row=26+POWERROWOFFSET, column=5, sticky=W)

		self.DISCHARGE_I = Label(self, text="DISCHARGE_I: ")
		self.DISCHARGE_I.grid(row=27+POWERROWOFFSET, column=1, sticky=W)
		self.CHARGE_I = Label(self, text="CHARGE_I   : ")
		self.CHARGE_I.grid(row=27+POWERROWOFFSET, column=3, sticky=W)
		self.THREEV3BUS_I = Label(self, text="3V3BUS_I   : ")
		self.THREEV3BUS_I.grid(row=27+POWERROWOFFSET, column=5, sticky=W)
		self.VBATT1_I = Label(self, text="VBATT1_I   : ")
		self.VBATT1_I.grid(row=27+POWERROWOFFSET, column=7, sticky=W)
		self.VBATT2_I = Label(self, text="VBATT2_I   : ")
		self.VBATT2_I.grid(row=27+POWERROWOFFSET, column=9, sticky=W)

		self.SA_YM_TEMP = Label(self, text="SA_Ym_TEMP: ")
		self.SA_YM_TEMP.grid(row=28+POWERROWOFFSET, column=1, sticky=W)
		self.SA_ZP_TEMP = Label(self, text="SA_Zp_TEMP: ")
		self.SA_ZP_TEMP.grid(row=28+POWERROWOFFSET, column=3, sticky=W)
		self.SA_ZM_TEMP = Label(self, text="SA_Zm_TEMP: ")
		self.SA_ZM_TEMP.grid(row=28+POWERROWOFFSET, column=5, sticky=W)
		self.SA_XP_TEMP = Label(self, text="SA_Xp_TEMP: ")
		self.SA_XP_TEMP.grid(row=28+POWERROWOFFSET, column=7, sticky=W)
		self.SA_YP_TEMP = Label(self, text="SA_Yp_TEMP: ")
		self.SA_YP_TEMP.grid(row=28+POWERROWOFFSET, column=9, sticky=W)

		self.THREEV3EPS_I = Label(self, text="3V3EPS_I: ")
		self.THREEV3EPS_I.grid(row=29+POWERROWOFFSET, column=1, sticky=W)
		self.FIVEV0EPS_I = Label(self, text="5V0BUS_I: ")
		self.FIVEV0EPS_I.grid(row=29+POWERROWOFFSET, column=3, sticky=W)

		self.HIST_SA_1_P_1 = Label(self, text="HIST_SA_1_P_1: ")
		self.HIST_SA_1_P_1.grid(row=30+POWERROWOFFSET, column=1, sticky=W)
		self.HIST_SA_1_P_2 = Label(self, text="HIST_SA_1_P_2: ")
		self.HIST_SA_1_P_2.grid(row=30+POWERROWOFFSET, column=3, sticky=W)
		self.HIST_SA_1_P_3 = Label(self, text="HIST_SA_1_P_3: ")
		self.HIST_SA_1_P_3.grid(row=30+POWERROWOFFSET, column=5, sticky=W)
		self.HIST_SA_1_P_4 = Label(self, text="HIST_SA_1_P_4: ")
		self.HIST_SA_1_P_4.grid(row=30+POWERROWOFFSET, column=7, sticky=W)
		self.HIST_SA_1_P_5 = Label(self, text="HIST_SA_1_P_5: ")
		self.HIST_SA_1_P_5.grid(row=30+POWERROWOFFSET, column=9, sticky=W)
		self.HIST_SA_1_P_6 = Label(self, text="HIST_SA_1_P_6: ")
		self.HIST_SA_1_P_6.grid(row=30+POWERROWOFFSET, column=11, sticky=W)

		self.HIST_SA_2_P_1 = Label(self, text="HIST_SA_2_P_1: ")
		self.HIST_SA_2_P_1.grid(row=31+POWERROWOFFSET, column=1, sticky=W)
		self.HIST_SA_2_P_2 = Label(self, text="HIST_SA_2_P_2: ")
		self.HIST_SA_2_P_2.grid(row=31+POWERROWOFFSET, column=3, sticky=W)
		self.HIST_SA_2_P_3 = Label(self, text="HIST_SA_2_P_3: ")
		self.HIST_SA_2_P_3.grid(row=31+POWERROWOFFSET, column=5, sticky=W)
		self.HIST_SA_2_P_4 = Label(self, text="HIST_SA_2_P_4: ")
		self.HIST_SA_2_P_4.grid(row=31+POWERROWOFFSET, column=7, sticky=W)
		self.HIST_SA_2_P_5 = Label(self, text="HIST_SA_2_P_5: ")
		self.HIST_SA_2_P_5.grid(row=31+POWERROWOFFSET, column=9, sticky=W)
		self.HIST_SA_2_P_6 = Label(self, text="HIST_SA_2_P_6: ")
		self.HIST_SA_2_P_6.grid(row=31+POWERROWOFFSET, column=11, sticky=W)

		self.HIST_SA_3_P_1 = Label(self, text="HIST_SA_3_P_1: ")
		self.HIST_SA_3_P_1.grid(row=32+POWERROWOFFSET, column=1, sticky=W)
		self.HIST_SA_3_P_2 = Label(self, text="HIST_SA_3_P_2: ")
		self.HIST_SA_3_P_2.grid(row=32+POWERROWOFFSET, column=3, sticky=W)
		self.HIST_SA_3_P_3 = Label(self, text="HIST_SA_3_P_3: ")
		self.HIST_SA_3_P_3.grid(row=32+POWERROWOFFSET, column=5, sticky=W)
		self.HIST_SA_3_P_4 = Label(self, text="HIST_SA_3_P_4: ")
		self.HIST_SA_3_P_4.grid(row=32+POWERROWOFFSET, column=7, sticky=W)
		self.HIST_SA_3_P_5 = Label(self, text="HIST_SA_3_P_5: ")
		self.HIST_SA_3_P_5.grid(row=32+POWERROWOFFSET, column=9, sticky=W)
		self.HIST_SA_3_P_6 = Label(self, text="HIST_SA_3_P_6: ")
		self.HIST_SA_3_P_6.grid(row=32+POWERROWOFFSET, column=11, sticky=W)

		self.HIST_BATT_V_1 = Label(self, text="HIST_BATT_V_1: ")
		self.HIST_BATT_V_1.grid(row=33+POWERROWOFFSET, column=1, sticky=W)
		self.HIST_BATT_V_2 = Label(self, text="HIST_BATT_V_2: ")
		self.HIST_BATT_V_2.grid(row=33+POWERROWOFFSET, column=3, sticky=W)
		self.HIST_BATT_V_3 = Label(self, text="HIST_BATT_V_3: ")
		self.HIST_BATT_V_3.grid(row=33+POWERROWOFFSET, column=5, sticky=W)
		self.HIST_BATT_V_4 = Label(self, text="HIST_BATT_V_4: ")
		self.HIST_BATT_V_4.grid(row=33+POWERROWOFFSET, column=7, sticky=W)
		self.HIST_BATT_V_5 = Label(self, text="HIST_BATT_V_5: ")
		self.HIST_BATT_V_5.grid(row=33+POWERROWOFFSET, column=9, sticky=W)
		self.HIST_BATT_V_6 = Label(self, text="HIST_BATT_V_6: ")
		self.HIST_BATT_V_6.grid(row=33+POWERROWOFFSET, column=11, sticky=W)

		self.HIST_BATT_I_1 = Label(self, text="HIST_BATT_I_1: ")
		self.HIST_BATT_I_1.grid(row=34+POWERROWOFFSET, column=1, sticky=W)
		self.HIST_BATT_I_2 = Label(self, text="HIST_BATT_I_2: ")
		self.HIST_BATT_I_2.grid(row=34+POWERROWOFFSET, column=3, sticky=W)
		self.HIST_BATT_I_3 = Label(self, text="HIST_BATT_I_3: ")
		self.HIST_BATT_I_3.grid(row=34+POWERROWOFFSET, column=5, sticky=W)
		self.HIST_BATT_I_4 = Label(self, text="HIST_BATT_I_4: ")
		self.HIST_BATT_I_4.grid(row=34+POWERROWOFFSET, column=7, sticky=W)
		self.HIST_BATT_I_5 = Label(self, text="HIST_BATT_I_5: ")
		self.HIST_BATT_I_5.grid(row=34+POWERROWOFFSET, column=9, sticky=W)
		self.HIST_BATT_I_6 = Label(self, text="HIST_BATT_I_6: ")
		self.HIST_BATT_I_6.grid(row=34+POWERROWOFFSET, column=11, sticky=W)


		#self.updatePower(test_string_health)
		Label(self, text="Misc data/Powerchunk: ").grid(row=100, column=1, sticky=W)



	def updateTile(self,data):
		OFFSET = 0
		self.S6_COUNT["text"] = "S6 Count		: " + data[0+OFFSET:3+OFFSET].hex()
		self.ACT_TILES["text"] = "ACT TILES   	: " + data[3+OFFSET:5+OFFSET].hex()
		self.FAULTED_TILES["text"] = "FAULTED TILES	: " + data[5+OFFSET:7+OFFSET].hex()
		self.FAULTED_COUNT1["text"] = "FAULTED COUNT 1	: " + data[7+OFFSET:9+OFFSET].hex()
		self.FAULTED_COUNT2["text"] = "FAULTED COUNT 2	: " + data[9+OFFSET:11+OFFSET].hex()

		self.FAULTED_COUNT3["text"] = "FAULTED COUNT 3	: " + data[11+OFFSET:13+OFFSET].hex()
		self.FAULTED_COUNT4["text"] = "FAULTED COUNT 4	: " + data[13+OFFSET:15+OFFSET].hex()
		self.FAULTED_COUNT5["text"] = "FAULTED COUNT 5	: " + data[15+OFFSET:17+OFFSET].hex()
		self.FAULTED_COUNT6["text"] = "FAULTED COUNT 6	: " + data[17+OFFSET:19+OFFSET].hex()
		self.FAULTED_COUNT7["text"] = "FAULTED COUNT 7	: " + data[19+OFFSET:21+OFFSET].hex()
		self.FAULTED_COUNT8["text"] = "FAULTED COUNT 8	: " + data[23+OFFSET:25+OFFSET].hex()
		self.FAULTS_INJECTED["text"] = "FAULTS INJECTED	: " + data[25+OFFSET:27+OFFSET].hex()
		self.TOTAL_FAULTS["text"] = "TOTAL FAULTS	: " + data[27+OFFSET:29+OFFSET].hex()
		self.MOVE_TILE_COUNT["text"] = "MOVE TILE COUNT	: " + data[29+OFFSET:31+OFFSET].hex()
		self.NEXT_SPARE["text"] = "NEXT SPARE	: " + data[31+OFFSET:32+OFFSET].hex()
		self.READBACK_FAULTS["text"] = "Readback Faults	: " + data[33+OFFSET:34+OFFSET].hex()
		self.WATCHDOG["text"] = "Watchdog		: " +data[34+OFFSET:35+OFFSET].hex()
		self.ACT_PROC1["text"] = "ACT PROC1	: " + data[35+OFFSET:36+OFFSET].hex()
		self.ACT_PROC2["text"] = "ACT PROC2	: " + data[36+OFFSET:37+OFFSET].hex()
		self.ACT_PROC3["text"] = "ACT PROC3	: " + data[37+OFFSET:38+OFFSET].hex()
		self.ACTPROCCNT1["text"] = "ACTPROCCNT1	: " + data[38+OFFSET:40+OFFSET].hex()
		self.ACTPROCCNT2["text"] = "ACTPROCCNT2	: " + data[40+OFFSET:42+OFFSET].hex()
		self.ACTPROCCNT3["text"] = "ACTPROCCNT3	: " + data[42+OFFSET:44+OFFSET].hex()
		self.VOTER_COUNTS["text"] = "VOTER COUNTS	: " + data[44+OFFSET:46+OFFSET].hex()
		self.CRC_TILE["text"] = "CRC		: " + data[46+OFFSET:48+OFFSET].hex()
		self.SYNC["text"] = "SYNC	: " + data[48+OFFSET:49+OFFSET].hex()




	def updateHealth(self,data):
		OFFSET = 0

		### VOLTAGES ###
		self.VOLTAGE_INS_IN["text"]	 = "VOLTAGE_INS_IN: " + str(int(data[2+OFFSET:4+OFFSET].hex(),16)  /1000)+" V"
		self.VOLTAGE_AVE_IN["text"]	 = "VOLTAGE_INS_IN: " + str(int(data[4+OFFSET:6+OFFSET].hex(),16)  /1000)+" V"
		self.VOLTAGE_MAX_IN["text"]	 = "VOLTAGE_INS_IN: " + str(int(data[6+OFFSET:8+OFFSET].hex(),16)  /1000)+" V"
		self.VOLTAGE_MIN_IN["text"]	 = "VOLTAGE_INS_IN: " + str(int(data[8+OFFSET:10+OFFSET].hex(),16) /1000)+" V"
		self.VOLTAGE_INS_3V3D["text"]   = "VOLTAGE_INS_3V3D: " + str(int(data[10+OFFSET:12+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_AVE_3V3D["text"]   = "VOLTAGE_INS_3V3D: " + str(int(data[12+OFFSET:14+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_MAX_3V3D["text"]   = "VOLTAGE_INS_3V3D: " + str(int(data[14+OFFSET:16+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_MIN_3V3D["text"]   = "VOLTAGE_INS_3V3D: " + str(int(data[16+OFFSET:18+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_INS_2V5D["text"]   = "VOLTAGE_INS_2V5D: " + str(int(data[18+OFFSET:20+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_AVE_2V5D["text"]   = "VOLTAGE_INS_2V5D: " + str(int(data[20+OFFSET:22+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_MAX_2V5D["text"]   = "VOLTAGE_INS_2V5D: " + str(int(data[22+OFFSET:24+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_MIN_2V5D["text"]   = "VOLTAGE_INS_2V5D: " + str(int(data[24+OFFSET:26+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_INS_1V8D["text"]   = "VOLTAGE_INS_1V8D: " + str(int(data[26+OFFSET:28+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_AVE_1V8D["text"]   = "VOLTAGE_INS_1V8D: " + str(int(data[28+OFFSET:30+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_MAX_1V8D["text"]   = "VOLTAGE_INS_1V8D: " + str(int(data[30+OFFSET:32+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_MIN_1V8D["text"]   = "VOLTAGE_INS_1V8D: " + str(int(data[32+OFFSET:34+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_INS_1V0SD["text"]  = "VOLTAGE_INS_1V0SD: " + str(int(data[34+OFFSET:36+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_AVE_1V0SD["text"]  = "VOLTAGE_INS_1V0SD: " + str(int(data[36+OFFSET:38+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_MAX_1V0SD["text"]  = "VOLTAGE_INS_1V0SD: " + str(int(data[38+OFFSET:40+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_MIN_1V0SD["text"]  = "VOLTAGE_INS_1V0SD: " + str(int(data[40+OFFSET:42+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_INS_0V95AD["text"] = "VOLTAGE_INS_0V95AD: " + str(int(data[42+OFFSET:44+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_AVE_0V95AD["text"] = "VOLTAGE_INS_0V95AD: " + str(int(data[44+OFFSET:46+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_MAX_0V95AD["text"] = "VOLTAGE_INS_0V95AD: " + str(int(data[46+OFFSET:48+OFFSET].hex(),16)/1000)+" V"
		self.VOLTAGE_MIN_0V95AD["text"] = "VOLTAGE_INS_0V95AD: " + str(int(data[48+OFFSET:50+OFFSET].hex(),16)/1000)+" V"

		### CURRENTS ###
		self.CURRENT_INS_IN["text"] = "CURRENT INS IN: " + str(int(data[48+2+OFFSET: 48+4+OFFSET].hex(),16))
		self.CURRENT_AVE_IN["text"] = "CURRENT AVE IN: " + str(int(data[48+4+OFFSET: 48+6+OFFSET].hex(),16))
		self.CURRENT_MAX_IN["text"] = "CURRENT MAX IN: " + str(int(data[48+6+OFFSET: 48+8+OFFSET].hex(),16))
		self.CURRENT_MIN_IN["text"] = "CURRENT MIN IN: " + str(int(data[48+8+OFFSET: 48+10+OFFSET].hex(),16))
		self.CURRENT_INS_3V3D["text"] = "CURRENT INS 3V3D: " + str(int(data[48+10+OFFSET:48+12+OFFSET].hex(),16))
		self.CURRENT_AVE_3V3D["text"] = "CURRENT AVE 3V3D: " + str(int(data[48+12+OFFSET:48+14+OFFSET].hex(),16))
		self.CURRENT_MAX_3V3D["text"] = "CURRENT MAX 3V3D: " + str(int(data[48+14+OFFSET:48+16+OFFSET].hex(),16))
		self.CURRENT_MIN_3V3D["text"] = "CURRENT MIN 3V3D: " + str(int(data[48+16+OFFSET:48+18+OFFSET].hex(),16))
		self.CURRENT_INS_2V5D["text"] = "CURRENT INS 2V5D: " + str(int(data[48+18+OFFSET:48+20+OFFSET].hex(),16))
		self.CURRENT_AVE_2V5D["text"] = "CURRENT AVE 2V5D: " + str(int(data[48+20+OFFSET:48+22+OFFSET].hex(),16))
		self.CURRENT_MAX_2V5D["text"] = "CURRENT MAX 2V5D: " + str(int(data[48+22+OFFSET:48+24+OFFSET].hex(),16))
		self.CURRENT_MIN_2V5D["text"] = "CURRENT MIN 2V5D: " + str(int(data[48+24+OFFSET:48+26+OFFSET].hex(),16))
		self.CURRENT_INS_1V8D["text"] = "CURRENT INS 1V8D: " + str(int(data[48+26+OFFSET:48+28+OFFSET].hex(),16))
		self.CURRENT_AVE_1V8D["text"] = "CURRENT AVE 1V8D: " + str(int(data[48+28+OFFSET:48+30+OFFSET].hex(),16))
		self.CURRENT_MAX_1V8D["text"] = "CURRENT MAX 1V8D: " + str(int(data[48+30+OFFSET:48+32+OFFSET].hex(),16))
		self.CURRENT_MIN_1V8D["text"] = "CURRENT MIN 1V8D: " + str(int(data[48+32+OFFSET:48+34+OFFSET].hex(),16))
		self.CURRENT_INS_1V0SD["text"] = "CURRENT INS 1V0SD: " + str(int(data[48+34+OFFSET:48+36+OFFSET].hex(),16))
		self.CURRENT_AVE_1V0SD["text"] = "CURRENT AVE 1V0SD: " + str(int(data[48+36+OFFSET:48+38+OFFSET].hex(),16))
		self.CURRENT_MAX_1V0SD["text"] = "CURRENT MAX 1V0SD: " + str(int(data[48+38+OFFSET:48+40+OFFSET].hex(),16))
		self.CURRENT_MIN_1V0SD["text"] = "CURRENT MIN 1V0SD: " + str(int(data[48+40+OFFSET:48+42+OFFSET].hex(),16))
		self.CURRENT_INS_0V95AD["text"] = "CURRENT INS 0V95AD: " + str(int(data[48+42+OFFSET:48+44+OFFSET].hex(),16))
		self.CURRENT_AVE_0V95AD["text"] = "CURRENT AVE 0V95AD: " + str(int(data[48+44+OFFSET:48+46+OFFSET].hex(),16))
		self.CURRENT_MAX_0V95AD["text"] = "CURRENT MAX 0V95AD: " + str(int(data[48+46+OFFSET:48+48+OFFSET].hex(),16))
		self.CURRENT_MIN_0V95AD["text"] = "CURRENT MIN 0V95AD: " + str(int(data[48+48+OFFSET:48+50+OFFSET].hex(),16))

		self.A7_TEMPERATURE["text"] = "A7 TEMPERATURE: " +  str(int(data[98+OFFSET:100+OFFSET].hex(),16))
		self.PC1_TEMPERATURE["text"] = "PC1 TEMPERATURE: " + str(int(data[100+OFFSET:102+OFFSET].hex(),16))
		self.PC2_TEMPERATURE["text"] = "PC2 TEMPERATURE: " + str(int(data[102+OFFSET:104+OFFSET].hex(),16))

		### RUNTIME ###
		self.DAYS["text"] = "DAYS: " + str(int(data[104+OFFSET:108+OFFSET].hex(),16))
		self.HOURS["text"] = "HOURS: " +  str(int(data[108+OFFSET:112+OFFSET].hex(),16))
		self.MINUTES["text"] = "MINUTES: " + str(int(data[112+OFFSET:116+OFFSET].hex(),16))
		self.SECONDS["text"] = "SECONDS: " + str(int(data[116+OFFSET:120+OFFSET].hex(),16))

		self.CRC_HEALTH["text"] = "CRC: " + str(int(data[120+OFFSET:122+OFFSET].hex(),16))

	def updatePower(self,data):
		DATAOFFSET = 0
		POWERROWOFFSET = 10

		#Initial set of data from EPS
		self.POWER_DATA["text"] = "POWER DATA: " + str(int(data[0+DATAOFFSET:4+DATAOFFSET].hex(),16))
		self.BYTES_SENT["text"] = "Bytes Sent	: " + str(int(data[4+DATAOFFSET:8+DATAOFFSET].hex(),16))
		self.BYTES_RECV["text"] = "Bytes Recv	: " + str(int(data[8+DATAOFFSET:10+DATAOFFSET].hex(),16))
		self.PKTS_SENT["text"] = "PKTS Sent		: " + str(int(data[10+DATAOFFSET:12+DATAOFFSET].hex(),16))
		self.PKTS_RECV["text"] = "PKTS Recv		: " + str(int(data[12+DATAOFFSET:14+DATAOFFSET].hex(),16))
		self.INVLD_PACK["text"] = "Invld Pack	: " + str(int(data[14+DATAOFFSET:16+DATAOFFSET].hex(),16))
		self.CRC_FAILS["text"] = "CRC Fails		: " + str(int(data[16+DATAOFFSET:18+DATAOFFSET].hex(),16))
		self.STATUS["text"] = "STATUS		: " + str(int(data[18+DATAOFFSET:20+DATAOFFSET].hex(),16))
		self.RESET_FLAG["text"] = "Reset Flag	: " + str(int(data[20+DATAOFFSET:22+DATAOFFSET].hex(),16))

		#SA1 SA2 SA3
		self.SA1_BOOST_V["text"] = "SA1 BOOST V: " + str(int(data[22+DATAOFFSET:24+DATAOFFSET].hex(),16))
		self.SA1_V["text"] = "SA1 V: " + str(int(data[24+DATAOFFSET:26+DATAOFFSET].hex(),16))
		self.SA2_BOOST_V["text"] = "SA2 BOOST V: " + str(int(data[26+DATAOFFSET:28+DATAOFFSET].hex(),16))
		self.SA2_V["text"] = "SA2 V: " + str(int(data[28+DATAOFFSET:30+DATAOFFSET].hex(),16))
		self.SA3_BOOST_V["text"] = "SA3 BOOST V: " + str(int(data[30+DATAOFFSET:32+DATAOFFSET].hex(),16))
		self.SA3_V["text"] = "SA3_V: " + str(int(data[32+DATAOFFSET:34+DATAOFFSET].hex(),16))

		#BATT TEMPS
		self.BATT2_TEMP["text"] = "BATT2 TEMP: " + str(int(data[34+DATAOFFSET:36+DATAOFFSET].hex(),16))
		self.BATT1_TEMP["text"] = "BATT1 TEMP: " + str(int(data[36+DATAOFFSET:38+DATAOFFSET].hex(),16))

		#BUS VOLTAGE
		self.FIVEV0BUS_V["text"] = "5V0BUS V: " + str(int(data[38+DATAOFFSET:40+DATAOFFSET].hex(),16))
		self.THREEV3BUS_V["text"] = "3V3BUS_V" + str(int(data[40+DATAOFFSET:42+DATAOFFSET].hex(),16))

		#BATTERY VOLTAGE
		self.VBATT2_V["text"] = "VBATT2 V: " + str(int(data[42+DATAOFFSET:44+DATAOFFSET].hex(),16))
		self.VBATT_V["text"] = "VBATT V: " + str(int(data[44+DATAOFFSET:46+DATAOFFSET].hex(),16))
		self.VBATT1_V["text"] = "VBATT1 V: " + str(int(data[46+DATAOFFSET:48+DATAOFFSET].hex(),16))

		#BUS TEMPS
		self.THREEV3BUS_TEMP["text"] = "3V3BUS TEMP: " + str(int(data[48+DATAOFFSET:50+DATAOFFSET].hex(),16))
		self.FIVEV0BUS_TEMP["text"] = "5V0BUS_TEMP: " + str(int(data[50+DATAOFFSET:52+DATAOFFSET].hex(),16))

		#3V3EPS
		self.THREEV3EPS_V["text"] = "3V3EPS V: " + str(int(data[52+DATAOFFSET:54+DATAOFFSET].hex(),16))

		#SAx_I
		self.SA1_I["text"] = "SA1_I: " + str(int(data[54+DATAOFFSET:56+DATAOFFSET].hex(),16))
		self.SA2_I["text"] = "SA2_I: " + str(int(data[56+DATAOFFSET:58+DATAOFFSET].hex(),16))
		self.SA3_I["text"] = "SA3_I: " + str(int(data[58+DATAOFFSET:60+DATAOFFSET].hex(),16))

		#CURRENT STATS
		self.DISCHARGE_I["text"] = "DISCHARGE_I: " + str(int(data[60+DATAOFFSET:62+DATAOFFSET].hex(),16))
		self.CHARGE_I["text"] = "CHARGE_I: " + str(int(data[62+DATAOFFSET:64+DATAOFFSET].hex(),16))
		self.THREEV3BUS_I["text"] = "3V3BUS_I: " + str(int(data[64+DATAOFFSET:66+DATAOFFSET].hex(),16))
		self.VBATT1_I["text"] = "VBATT1_I: " + str(int(data[66+DATAOFFSET:68+DATAOFFSET].hex(),16))
		self.VBATT2_I["text"] = "VBATT2_I: " + str(int(data[68+DATAOFFSET:70+DATAOFFSET].hex(),16))

		#SA TEMPS
		self.SA_YM_TEMP["text"] = "SA_YM_TEMP: " + str(int(data[70+DATAOFFSET:72+DATAOFFSET].hex(),16))
		self.SA_ZP_TEMP["text"] = "SA_ZP_TEMP: " + str(int(data[72+DATAOFFSET:74+DATAOFFSET].hex(),16))
		self.SA_ZM_TEMP["text"] = "SA_ZM_TEMP: " + str(int(data[74+DATAOFFSET:76+DATAOFFSET].hex(),16))
		self.SA_XP_TEMP["text"] = "SA_XP_TEMP: " + str(int(data[76+DATAOFFSET:78+DATAOFFSET].hex(),16))
		self.SA_YP_TEMP["text"] = "SA_YP_TEMP: " + str(int(data[78+DATAOFFSET:80+DATAOFFSET].hex(),16))

		#3V3EPS_I
		self.THREEV3EPS_I["text"] = "3V3EPS_I: " + str(int(data[80+DATAOFFSET:82+DATAOFFSET].hex(),16))
		self.FIVEV0EPS_I["text"] = "5V0EPS_I: " + str(int(data[82+DATAOFFSET:84+DATAOFFSET].hex(),16))

		#HIST_SA_1
		self.HIST_SA_1_P_1["text"] = "HIST SA 1 P 1: " + str(int(data[84+DATAOFFSET:86+DATAOFFSET].hex(),16))
		self.HIST_SA_1_P_2["text"] = "HIST SA 1 P 2: " + str(int(data[86+DATAOFFSET:88+DATAOFFSET].hex(),16))
		self.HIST_SA_1_P_3["text"] = "HIST SA 1 P 3: " + str(int(data[88+DATAOFFSET:90+DATAOFFSET].hex(),16))
		self.HIST_SA_1_P_4["text"] = "HIST SA 1 P 4: " + str(int(data[90+DATAOFFSET:92+DATAOFFSET].hex(),16))
		self.HIST_SA_1_P_5["text"] = "HIST SA 1 P 5: " + str(int(data[92+DATAOFFSET:94+DATAOFFSET].hex(),16))
		self.HIST_SA_1_P_6["text"] = "HIST SA 1 P 6: " + str(int(data[94+DATAOFFSET:96+DATAOFFSET].hex(),16))

		#HIST_SA_2
		self.HIST_SA_2_P_1["text"] = "HIST SA 2 P 1: " + str(int(data[96+DATAOFFSET:98+DATAOFFSET].hex(),16))
		self.HIST_SA_2_P_2["text"] = "HIST SA 2 P 2: " + str(int(data[98+DATAOFFSET:100+DATAOFFSET].hex(),16))
		self.HIST_SA_2_P_3["text"] = "HIST SA 2 P 3: " + str(int(data[100+DATAOFFSET:102+DATAOFFSET].hex(),16))
		self.HIST_SA_2_P_4["text"] = "HIST SA 2 P 4: " + str(int(data[102+DATAOFFSET:104+DATAOFFSET].hex(),16))
		self.HIST_SA_2_P_5["text"] = "HIST SA 2 P 5: " + str(int(data[104+DATAOFFSET:106+DATAOFFSET].hex(),16))
		self.HIST_SA_2_P_6["text"] = "HIST SA 2 P 6: " + str(int(data[106+DATAOFFSET:108+DATAOFFSET].hex(),16))

		#HIST_SA_3
		self.HIST_SA_3_P_1["text"] = "HIST SA 3 P 1" + str(int(data[108+DATAOFFSET:110+DATAOFFSET].hex(),16))
		self.HIST_SA_3_P_2["text"] = "HIST SA 3 P 2" + str(int(data[110+DATAOFFSET:112+DATAOFFSET].hex(),16))
		self.HIST_SA_3_P_3["text"] = "HIST SA 3 P 3" + str(int(data[112+DATAOFFSET:114+DATAOFFSET].hex(),16))
		self.HIST_SA_3_P_4["text"] = "HIST SA 3 P 4" + str(int(data[114+DATAOFFSET:116+DATAOFFSET].hex(),16))
		self.HIST_SA_3_P_5["text"] = "HIST SA 3 P 5" + str(int(data[116+DATAOFFSET:118+DATAOFFSET].hex(),16))
		self.HIST_SA_3_P_6["text"] = "HIST SA 3 P 6" + str(int(data[118+DATAOFFSET:120+DATAOFFSET].hex(),16))

		#HIST_BATT_V
		self.HIST_BATT_V_1["text"] = "HIST_BATT_V_1: " + str(int(data[120+DATAOFFSET:122+DATAOFFSET].hex(),16))
		self.HIST_BATT_V_2["text"] = "HIST_BATT_V_2: " + str(int(data[122+DATAOFFSET:124+DATAOFFSET].hex(),16))
		self.HIST_BATT_V_3["text"] = "HIST_BATT_V_3: " + str(int(data[124+DATAOFFSET:126+DATAOFFSET].hex(),16))
		self.HIST_BATT_V_4["text"] = "HIST_BATT_V_4: " + str(int(data[126+DATAOFFSET:128+DATAOFFSET].hex(),16))
		self.HIST_BATT_V_5["text"] = "HIST_BATT_V_5: " + str(int(data[128+DATAOFFSET:130+DATAOFFSET].hex(),16))
		self.HIST_BATT_V_6["text"] = "HIST_BATT_V_6: " + str(int(data[130+DATAOFFSET:132+DATAOFFSET].hex(),16))

		#HIST_BATT_I
		self.HIST_BATT_I_1["text"] = "HIST_BATT_I_1: " + str(int(data[132+DATAOFFSET:134+DATAOFFSET].hex(),16))
		self.HIST_BATT_I_2["text"] = "HIST_BATT_I_2: " + str(int(data[134+DATAOFFSET:136+DATAOFFSET].hex(),16))
		self.HIST_BATT_I_3["text"] = "HIST_BATT_I_3: " + str(int(data[136+DATAOFFSET:138+DATAOFFSET].hex(),16))
		self.HIST_BATT_I_4["text"] = "HIST_BATT_I_4: " + str(int(data[138+DATAOFFSET:140+DATAOFFSET].hex(),16))
		self.HIST_BATT_I_5["text"] = "HIST_BATT_I_5: " + str(int(data[140+DATAOFFSET:142+DATAOFFSET].hex(),16))
		self.HIST_BATT_I_6["text"] = "HIST_BATT_I_6: " + str(int(data[142+DATAOFFSET:144+DATAOFFSET].hex(),16))



	def updateMisc(self,data):
		pass
		#self.["text"] = "" +  = Label(self, justify=LEFT, wraplength=400, text=data.hex()).grid(row=100, column=2,sticky=W)

	def clock(self):
			self.timelabel = Label(self,height=3,bg="white", text=datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")).grid(row=1, column=2)				#goal is to update the clock constantly
			self.after(500,self.clock)



	def framcount(self):
	#will change this to represent the number of times that we have read data from the tcp port later
		DataGui.framcount += 1

	def threadedclock(self):


		updatetheclock = threading.Thread(target=self.clock)
		updatetheclock.isDaemon()
		updatetheclock.run()

	def lastpacketRecieved(self,data):
		Label(self, justify=LEFT, wraplength=800, text=data).grid(row=1, column=4,sticky=W)

class readSingle(threading.Thread):
	#With our current setup in the lab we cannot use the readline method
	#will not capture the data that we wantself.

	#Also need to make sure that
	def run(self):
		try:
			while(True):
				data = USB.readline(2)
				#print(f"{data}")
				if(data == b'He'):
					#can't use readline here, will not recieve full chunk of
					#data from stack
					#datastring = USB.read(6)	#get rid of radio header
					datastring = b'He' + USB.read(210)
					now = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")
					print(f"{now}\nlength {len(datastring)}\ndata: {datastring.hex()}")
					if(len(datastring) < 110):
						print("Tile data\n")
						gui.updateTile(datastring)
						gui.lastpacketRecieved(now)

					elif(len(datastring) < 209):
						print("Health datastring\n")
						gui.updateHealth(datastring)
						gui.lastpacketRecieved(now)

					elif(len(datastring) >= 209):
						print("Power datastring\n")
						gui.updatePower(datastring)
						gui.updateMisc(datastring)
						gui.lastpacketRecieved(now)

					else:
						print("Miscellaneous datastring\n")
						gui.updateMisc(datastring)
						gui.lastpacketRecieved(now)




		except:
			USB.close()
			print("Program exiting")
			exit()


if __name__ == "__main__" :

	time = datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")

	root = Tk()
	gui = DataGui(root)
	startup = 0

	test = readSingle()
	test.start()
	gui.mainloop()

	#need to figure out how to update values on the run
