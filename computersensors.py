
import time
import psutil
import datetime
from tkinter import *


class DataGui(Frame):

	def __init__(self, parent, *args, **kwargs):
		Frame.__init__(self, parent, *args, **kwargs)

		self.root = parent
		self.root.title("Data Gui")

		self.grid(column=0,row=0, sticky='nsew')


		self.timevar = StringVar()
		self.timevar.set("test")
		self.clock()
		self.processLoad()

		Label(self,height=3,bg="white", text="Last Recieved: ").grid(row=1, column=3,sticky=W)
		self.TIMELABEL = Label(self, text="Time:	")
		self.TIMELABEL.grid(row=1, column=1, sticky=W)

		self.TILE_DATA = Label(self, text="CPU Load: ")
		self.TILE_DATA.grid(row=10, column=1,sticky=W)
		self.S6_COUNT = Label(self, text="CPU Temp: ")
		self.S6_COUNT.grid(row=10, column=3,sticky=W)
		self.ACT_TILES = Label(self, text="MEM Load: ")
		self.ACT_TILES.grid(row=11, column=1,sticky=W)


		#self.updatePower(test_string_health)
		Label(self, text="Misc data/Powerchunk: ").grid(row=100, column=1, sticky=W)



	def updateTile(self,data):
		OFFSET = 18
		self.S6_COUNT["text"] = "S6 Count	: " + data[0+OFFSET:3+OFFSET].hex()




	def updateHealth(self,data):
		OFFSET = 15

		### VOLTAGES ###
		self.VOLTAGE_INS_IN["text"]	 = "VOLTAGE_INS_IN: " + str(int(data[2+OFFSET:4+OFFSET].hex(),16)  /1000)+" V"

	def updatePower(self,data):
		DATAOFFSET = 12
		POWERROWOFFSET = 10

		#Initial set of data from EPS
		self.POWER_DATA["text"] = "POWER DATA: " + str(int(data[0+DATAOFFSET:4+DATAOFFSET].hex(),16))


	def updateMisc(self,data):
		pass
		#self.["text"] = "" +  = Label(self, justify=LEFT, wraplength=400, text=data.hex()).grid(row=100, column=2,sticky=W)

	def clock(self):
		self.TIMELABEL = Label(self,height=3,bg="white", text=datetime.datetime.now().strftime("%I:%M:%S%p on %B %d, %Y")).grid(row=1, column=2)	#goal is to update the clock constantly
		self.after(500,self.clock)

	def lastpacketRecieved(self,data):
		Label(self, justify=LEFT, wraplength=800, text=data).grid(row=1, column=4,sticky=W)



	def processLoad(self):
		self.TIMELABEL["text"] = psutil.cpu_percent(interval=1)
		#self.after(500, self.processLoad)

	def testloop():
		for i in range(0,10):
			time.sleep(.5)
			try:
				print(psutil.cpu_percent(interval=1))
			except KeyboardInterrupt:
				print("should be exitiing now")
				break




if __name__ == "__main__":

	root = Tk()

	gui = DataGui(root)
	gui.mainloop()
