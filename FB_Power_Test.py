#   This file is pulled from the public Titan files
#   This is the file that MH used to test the EPS board
#

import serial
import datetime
import thread
from time import sleep
import os

if not os.path.exists('FIREBIRD_Power_Data'):
    os.makedirs('FIREBIRD_Power_Data')

### Connection settings ######
port = "COM1"
baud = 38400
##############################

### Poll Rate (in seconds) ###
poll = 5
##############################

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

Coeff['33V_BUS_I'] =    [-11.02,    1.1653,    0.00003, 'mA']
Coeff['5V_BUS_I'] =     [-15.564,   1.183011,  -0.000293, 'mA']

Coeff['VBATT_V'] =      [-0.0008,   0.0144,  -0.000001, 'V']
Coeff['VBATT_Discharge'] =      [-14.8,   1.726,  0.00008, 'mA']

Coeff['VBATT1_V'] =      [-0.3529,   0.0154, -0.000002, 'V']
Coeff['VBATT1_I'] =      [-15.768,   1.7367, -0.00005, 'mA']

Coeff['VBATT2_V'] =      [-0.3529,   0.0154, -0.000002, 'V']
Coeff['VBATT2_I'] =      [-6.6625,   0.7005, -0.000005, 'mA']

Coeff['EPS_WDT'] =      [0,         0.0115833333333333, 'Hours']
Coeff['None'] =         [0,         1,                  '']


cmd_bytes = [  0xC0, 0x00, 0x00, 0x00, 0x06, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0xBC, 0xC0]
cmd_str = ""
for b in cmd_bytes:
    cmd_str += chr(b)

END = chr(0xC0)
ESC = chr(0xDB)
ESC_END = chr(0xDC)
ESC_ESC = chr(0xDD)

packets = []

global first_packet
first_packet = True

global fname
fname = "FIREBIRD_Power_Data\\Converted_Data_{date}.csv".format(date=datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"))

def Convert(data, offset, size, coeff_name):

    bytes_ = data[offset:offset+size]

    raw = 0
    for i in range(0,size):
        raw += ord(bytes_[size -i -1]) * (2** (8*i))

    converted = 0
    for i in range(len(Coeff[coeff_name]) -1):
        converted += Coeff[coeff_name][i] * (raw ** i)

    return [converted, Coeff[coeff_name][-1]]

class PowerPacket:

    def __init__(self, bytes_in):


        self.dt = datetime.datetime.now()

        packets.append(self)

        # save input bytes
        self.data =[]
        last_byte = 0x00
        for b in bytes_in:

            # un-stuff bytes
            if(b == ESC):
                last_byte = ESC
            else:
                if(last_byte == ESC and b == ESC_END):
                    self.data.append(END)
                    last_byte = END
                elif(last_byte == ESC and b == ESC_ESC):
                    self.data.append(ESC)
                    last_byte = ESC
                else:
                    self.data.append(b)
                    last_byte = b


        if(len(self.data) != 148):
            print "Bad Packet"
            print len(self.data)
            return None

        self.tlm = {}

        self.tlm['BYTES_SENT'] =            Convert(self.data,    1,  4, 'None')
        self.tlm['BYTES_RECIEVED'] =        Convert(self.data,    5,  4, 'None')
        self.tlm['PKTS_SENT'] =             Convert(self.data,    9,  2, 'None')
        self.tlm['PKTS_RECIEVED'] =         Convert(self.data,   11,  2, 'None')
        self.tlm['INVALID_PKTS_RECIEVED'] = Convert(self.data,   13,  2, 'None')
        self.tlm['CRC_FAILS'] =             Convert(self.data,   15,  2, 'None')
        self.tlm['STATUS'] =                Convert(self.data,   17,  2, 'None')
        self.tlm['EPS_PIC_RESET_FLAGS'] =   Convert(self.data,   19,  2, 'None')
        self.tlm['EPS_WDT'] =               Convert(self.data,   21,  2, 'EPS_WDT')

        self.tlm['SA1_BOOST_V'] =           Convert(self.data,   23,  2, 'LARGE_V')
        self.tlm['SA1_V'] =                 Convert(self.data,   25,  2, 'LARGE_V')
        self.tlm['SA2_BOOST_V'] =           Convert(self.data,   27,  2, 'LARGE_V')
        self.tlm['SA2_V'] =                 Convert(self.data,   29,  2, 'LARGE_V')
        self.tlm['SA3_V'] =                 Convert(self.data,   31,  2, 'LARGE_V')
        self.tlm['SA3_BOOST_V'] =           Convert(self.data,   33,  2, 'LARGE_V')

        self.tlm['BATT2_TEMP'] =            Convert(self.data,   35,  2, 'AD590_TEMP')
        self.tlm['BATT1_TEMP'] =            Convert(self.data,   37,  2, 'AD590_TEMP')

        self.tlm['5VBUS_V'] =               Convert(self.data,   39,  2, 'STD_V')
        self.tlm['33VBUS_V'] =              Convert(self.data,   41,  2, 'STD_V')

        self.tlm['VBATT2_V'] =              Convert(self.data,   43,  2, 'VBATT2_V')
        self.tlm['VBATT_V'] =               Convert(self.data,   45,  2, 'VBATT_V')
        self.tlm['VBATT1_V'] =              Convert(self.data,   47,  2, 'VBATT1_V')

        self.tlm['33VBUS_TEMP'] =           Convert(self.data,   49,  2, 'BUS_TEMP')
        self.tlm['5VBUS_TEMP'] =            Convert(self.data,   51,  2, 'BUS_TEMP')

        self.tlm['33VEPS_V'] =              Convert(self.data,   53,  2, 'STD_V')

        self.tlm['SA1_I'] =                 Convert(self.data,   55,  2, 'STD_I')
        self.tlm['SA2_I'] =                 Convert(self.data,   57,  2, 'STD_I')
        self.tlm['SA3_I'] =                 Convert(self.data,   59,  2, 'STD_I')

        self.tlm['DISCHARGE_I'] =           Convert(self.data,   61,  2, 'VBATT_Discharge')
        self.tlm['CHARGE_I'] =              Convert(self.data,   63,  2, 'VBATT_Discharge')
        self.tlm['33VBUS_I'] =              Convert(self.data,   65,  2, '33V_BUS_I')
        self.tlm['VBATT1_I'] =              Convert(self.data,   67,  2, 'VBATT1_I')
        self.tlm['VBATT2_I'] =              Convert(self.data,   69,  2, 'VBATT2_I')

        self.tlm['SA_Ym_TEMP'] =            Convert(self.data,   71,  2, 'SA_TEMP')
        self.tlm['SA_Zp_TEMP'] =            Convert(self.data,   73,  2, 'SA_TEMP')
        self.tlm['SA_Zm_TEMP'] =            Convert(self.data,   75,  2, 'SA_TEMP')
        self.tlm['SA_Xp_TEMP'] =            Convert(self.data,   77,  2, 'SA_TEMP')
        self.tlm['SA_Yp_TEMP'] =            Convert(self.data,   79,  2, 'SA_TEMP')

        self.tlm['33VEPS_I'] =              Convert(self.data,   81,  2, '33EPS_I')
        self.tlm['5VBUS_I'] =               Convert(self.data,   83,  2, '5V_BUS_I')

        self.tlm['HIST_SA_1_P_1'] =         Convert(self.data,   85,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_1_P_2'] =         Convert(self.data,   87,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_1_P_3'] =         Convert(self.data,   89,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_1_P_4'] =         Convert(self.data,   91,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_1_P_5'] =         Convert(self.data,   93,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_1_P_6'] =         Convert(self.data,   95,  2, 'HIST_SA_P')

        self.tlm['HIST_SA_2_P_1'] =         Convert(self.data,   97,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_2_P_2'] =         Convert(self.data,   99,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_2_P_3'] =         Convert(self.data,  101,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_2_P_4'] =         Convert(self.data,  103,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_2_P_5'] =         Convert(self.data,  105,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_2_P_6'] =         Convert(self.data,  107,  2, 'HIST_SA_P')

        self.tlm['HIST_SA_3_P_1'] =         Convert(self.data,  109,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_3_P_2'] =         Convert(self.data,  111,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_3_P_3'] =         Convert(self.data,  113,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_3_P_4'] =         Convert(self.data,  115,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_3_P_5'] =         Convert(self.data,  117,  2, 'HIST_SA_P')
        self.tlm['HIST_SA_3_P_6'] =         Convert(self.data,  119,  2, 'HIST_SA_P')

        self.tlm['HIST_BATT_V_1'] =         Convert(self.data,  121,  2, 'STD_V')
        self.tlm['HIST_BATT_V_2'] =         Convert(self.data,  123,  2, 'STD_V')
        self.tlm['HIST_BATT_V_3'] =         Convert(self.data,  125,  2, 'STD_V')
        self.tlm['HIST_BATT_V_4'] =         Convert(self.data,  127,  2, 'STD_V')
        self.tlm['HIST_BATT_V_5'] =         Convert(self.data,  129,  2, 'STD_V')
        self.tlm['HIST_BATT_V_6'] =         Convert(self.data,  131,  2, 'STD_V')

        self.tlm['HIST_BATT_I_1'] =         Convert(self.data,  133,  2, 'STD_I')
        self.tlm['HIST_BATT_I_2'] =         Convert(self.data,  135,  2, 'STD_I')
        self.tlm['HIST_BATT_I_3'] =         Convert(self.data,  137,  2, 'STD_I')
        self.tlm['HIST_BATT_I_4'] =         Convert(self.data,  139,  2, 'STD_I')
        self.tlm['HIST_BATT_I_5'] =         Convert(self.data,  141,  2, 'STD_I')
        self.tlm['HIST_BATT_I_6'] =         Convert(self.data,  143,  2, 'STD_I')


        # sort the dictionary by key
        self.keys_sorted = sorted(self.tlm)

        ### Display converted data
        print 50*"\n"

        for k in key_order:
            if(len(k) != 0):
                print "{k}{s}{v:10.3f} {u}".format(k=k, s=" "*(30-len(k)), v=self.tlm[k][0], u=self.tlm[k][1])
            else:
                print ""

        ### Log converted

        global first_packet
        global fname

        if first_packet:
            first_packet = False

            s = "Date, "
            for k in self.keys_sorted:
                s += "{k}, ".format(k=k)

            s += "\n"
            try:
                with open(fname, 'w') as f:
                    f.write(s)
            except:
                print "\n***\nCould not write to: " + fname + "\n***"


        s = "{date}, ".format(date=self.dt.strftime("%Y-%m-%d %H:%M:%S"))

        for k in self.keys_sorted:
            s += "{v:.3f}, ".format(k=self.tlm[k], v=self.tlm[k][0])

        try:
            with open(fname, 'a') as f:
                f.write(s + "\n")
        except:
            print "\n***\nCould not write to: " + fname + "\n***"


### main loop ###

while True:
    ser = serial.Serial(port, baud, timeout=0.01)
    fname_raw = "FIREBIRD_Power_Data\\Raw_Data_{date}.txt".format(date=datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S"))



    while ser.isOpen:
        ser.write(cmd_str)
        sleep(0.5)
        data = ser.read(255)
        PowerPacket(data)

        s = "{date} ".format(date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        for d in data:
            s = s + "{0:02X} ".format(ord(d))

        s = s +"\n"

        try:
            with open(fname_raw, 'a') as f:
                    f.write(s)
        except:
            print "\n***\nCould not write to: " + fname_raw + "\n***"

        #print s +"\n"

        sleep(poll -0.5)
