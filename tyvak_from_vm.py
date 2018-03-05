#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Tyvak USRP Ground Station efffd4a
# Author: Matthew Handley (matt.handley@tyvak.com)
# Description: Configurable dual-channel FSK/GFSK AX.25 Packet Transceiver
# Generated: Thu Dec  8 19:12:28 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from approx_power import approx_power  # grc-generated hier_block
from demod_decode import demod_decode  # grc-generated hier_block
from encode_mod import encode_mod  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
from tx_tone import tx_tone  # grc-generated hier_block
import ConfigParser
import math
import numpy
import sip
import subprocess
import threading
import time
import tyvak


class Tyvak_GS(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Tyvak USRP Ground Station efffd4a")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Tyvak USRP Ground Station efffd4a")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Tyvak_GS")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.decm = decm = 6
        self.ch2_tx_freq = ch2_tx_freq = 437425000
        self.ch2_rx_freq = ch2_rx_freq = 437425000
        self.ch1_tx_freq = ch1_tx_freq = 437220000
        self.ch1_rx_freq = ch1_rx_freq = 437220000
        self.tx_delta_abs = tx_delta_abs = abs(ch1_tx_freq - ch2_tx_freq)
        self.samp_rate = samp_rate = 403.225806451613e3 / decm
        self.rx_delta_abs = rx_delta_abs = abs(ch1_rx_freq - ch2_rx_freq)
        self.ch2_tx_en = ch2_tx_en = int((ch2_tx_freq > 0) and (tx_delta_abs < (samp_rate*decm)))
        self.ch2_rx_en = ch2_rx_en = int((ch2_rx_freq > 0) and (rx_delta_abs < (samp_rate*decm)))
        self.ch2_h_raw = ch2_h_raw = 50
        self.ch2_baud_raw = ch2_baud_raw = 9600
        self.ch1_tx_en = ch1_tx_en = int(ch1_tx_freq > 0)
        self.ch1_rx_en = ch1_rx_en = int(ch1_rx_freq > 0)
        self.ch1_h_raw = ch1_h_raw = 50
        self.ch1_baud_raw = ch1_baud_raw = 9600
        self.cfg_filename = cfg_filename = "Tyvak_GS.cfg"
        self._water_range_config_config = ConfigParser.ConfigParser()
        self._water_range_config_config.read(cfg_filename)
        try: water_range_config = self._water_range_config_config.getfloat("settings", "water_range")
        except: water_range_config = 70
        self.water_range_config = water_range_config
        self._water_max_config_config = ConfigParser.ConfigParser()
        self._water_max_config_config.read(cfg_filename)
        try: water_max_config = self._water_max_config_config.getfloat("settings", "water_max")
        except: water_max_config = -30
        self.water_max_config = water_max_config
        self.usrp_tx = usrp_tx = (ch1_tx_freq*ch1_tx_en + ch2_tx_freq*ch2_tx_en) / max(1, (ch1_tx_en + ch2_tx_en))
        self.usrp_rx = usrp_rx = (ch1_rx_freq*ch1_rx_en + ch2_rx_freq*ch2_rx_en) / max(1, (ch1_rx_en + ch2_rx_en))
        self.ch2_tx_corr = ch2_tx_corr = 0
        self._ch2_threshold_config_config = ConfigParser.ConfigParser()
        self._ch2_threshold_config_config.read(cfg_filename)
        try: ch2_threshold_config = self._ch2_threshold_config_config.getfloat("settings", "ch2_threshold")
        except: ch2_threshold_config = -90
        self.ch2_threshold_config = ch2_threshold_config
        self.ch2_rx_corr = ch2_rx_corr = 0
        self._ch2_fft_range_config_config = ConfigParser.ConfigParser()
        self._ch2_fft_range_config_config.read(cfg_filename)
        try: ch2_fft_range_config = self._ch2_fft_range_config_config.getfloat("settings", "ch2_fft_range")
        except: ch2_fft_range_config = 70
        self.ch2_fft_range_config = ch2_fft_range_config
        self._ch2_fft_max_config_config = ConfigParser.ConfigParser()
        self._ch2_fft_max_config_config.read(cfg_filename)
        try: ch2_fft_max_config = self._ch2_fft_max_config_config.getfloat("settings", "ch2_fft_max")
        except: ch2_fft_max_config = -30
        self.ch2_fft_max_config = ch2_fft_max_config
        self.ch2_bt = ch2_bt = max(0.01, ch2_h_raw / 100.0)
        self.ch2_baud = ch2_baud = max(9600, ch2_baud_raw)
        self.ch1_tx_gain = ch1_tx_gain = 30
        self.ch1_tx_corr = ch1_tx_corr = 0
        self._ch1_threshold_config_config = ConfigParser.ConfigParser()
        self._ch1_threshold_config_config.read(cfg_filename)
        try: ch1_threshold_config = self._ch1_threshold_config_config.getfloat("settings", "ch1_threshold")
        except: ch1_threshold_config = -90
        self.ch1_threshold_config = ch1_threshold_config
        self.ch1_rx_gain = ch1_rx_gain = 20
        self.ch1_rx_corr = ch1_rx_corr = 0
        self._ch1_fft_range_config_config = ConfigParser.ConfigParser()
        self._ch1_fft_range_config_config.read(cfg_filename)
        try: ch1_fft_range_config = self._ch1_fft_range_config_config.getfloat("settings", "ch1_fft_range")
        except: ch1_fft_range_config = 70
        self.ch1_fft_range_config = ch1_fft_range_config
        self._ch1_fft_max_config_config = ConfigParser.ConfigParser()
        self._ch1_fft_max_config_config.read(cfg_filename)
        try: ch1_fft_max_config = self._ch1_fft_max_config_config.getfloat("settings", "ch1_fft_max")
        except: ch1_fft_max_config = -30
        self.ch1_fft_max_config = ch1_fft_max_config
        self.ch1_bt = ch1_bt = max(0.01, ch1_h_raw / 100.0)
        self.ch1_baud = ch1_baud = max(9600, ch1_baud_raw)
        self.water_range = water_range = water_range_config
        self.water_max = water_max = water_max_config
        self.version = version = subprocess.check_output("cd ~/gr-tyvak/; git describe --always --long", shell=True, executable="/bin/bash").strip().split("-g")[-1]
        self.usrp_tx_label = usrp_tx_label = "{:3.4f} MHz  ".format(usrp_tx / 1e6)
        self.usrp_rx_label = usrp_rx_label = "{:3.4f} MHz  ".format(usrp_rx / 1e6)
        self._usrp_addr_config = ConfigParser.ConfigParser()
        self._usrp_addr_config.read(cfg_filename)
        try: usrp_addr = self._usrp_addr_config.get("usrp", "addr")
        except: usrp_addr = "addr=192.168.20.2"
        self.usrp_addr = usrp_addr
        self._rx_data_tcp_ip_config = ConfigParser.ConfigParser()
        self._rx_data_tcp_ip_config.read("Tyvak_GS.cfg")
        try: rx_data_tcp_ip = self._rx_data_tcp_ip_config.get("rx", "ip")
        except: rx_data_tcp_ip = "127.0.0.1"
        self.rx_data_tcp_ip = rx_data_tcp_ip
        self._period_config_config = ConfigParser.ConfigParser()
        self._period_config_config.read(cfg_filename)
        try: period_config = self._period_config_config.getfloat("settings", "period")
        except: period_config = 5
        self.period_config = period_config
        self.period = period = 5
        self._config_tcp_ip_config = ConfigParser.ConfigParser()
        self._config_tcp_ip_config.read(cfg_filename)
        try: config_tcp_ip = self._config_tcp_ip_config.get("tx", "ip")
        except: config_tcp_ip = "127.0.0.1"
        self.config_tcp_ip = config_tcp_ip
        self.ch2_tx_freq_label = ch2_tx_freq_label = "{:3.4f} MHz  ".format((ch2_tx_freq+ch2_tx_corr) / 1e6)
        self.ch2_tx_en_label = ch2_tx_en_label = bool(ch2_tx_en)
        self.ch2_threshold = ch2_threshold = ch2_threshold_config
        self.ch2_rx_freq_label = ch2_rx_freq_label = "{:3.4f} MHz  ".format((ch2_rx_freq+ch2_rx_corr) / 1e6)
        self.ch2_rx_en_label = ch2_rx_en_label = bool(ch2_rx_en)
        self._ch2_rx_data_tcp_port_config = ConfigParser.ConfigParser()
        self._ch2_rx_data_tcp_port_config.read("Tyvak_GS.cfg")
        try: ch2_rx_data_tcp_port = self._ch2_rx_data_tcp_port_config.getint("rx", "ch2_port")
        except: ch2_rx_data_tcp_port = 4102
        self.ch2_rx_data_tcp_port = ch2_rx_data_tcp_port
        self.ch2_pwr = ch2_pwr = -130
        self.ch2_fft_range = ch2_fft_range = ch2_fft_range_config
        self.ch2_fft_max = ch2_fft_max = ch2_fft_max_config
        self._ch2_config_tcp_port_config = ConfigParser.ConfigParser()
        self._ch2_config_tcp_port_config.read(cfg_filename)
        try: ch2_config_tcp_port = self._ch2_config_tcp_port_config.getint("tx", "ch2_port")
        except: ch2_config_tcp_port = 4002
        self.ch2_config_tcp_port = ch2_config_tcp_port
        self.ch2_bt_label_0 = ch2_bt_label_0 = "{0}".format(ch2_bt)
        self.ch2_baud_label_0 = ch2_baud_label_0 = "{0}  ".format(ch2_baud)
        self.ch1_tx_gain_label = ch1_tx_gain_label = "{0:2.0f} dB  ".format(ch1_tx_gain)
        self.ch1_tx_freq_label = ch1_tx_freq_label = "{:3.4f} MHz  ".format((ch1_tx_freq+ch1_tx_corr) / 1e6)
        self.ch1_tx_en_label = ch1_tx_en_label = bool(ch1_tx_en)
        self.ch1_threshold = ch1_threshold = ch1_threshold_config
        self.ch1_rx_gain_label = ch1_rx_gain_label = "{0:2.0f} dB  ".format(ch1_rx_gain)
        self.ch1_rx_freq_label = ch1_rx_freq_label = "{:3.4f} MHz  ".format((ch1_rx_freq+ch1_rx_corr) / 1e6)
        self.ch1_rx_en_label = ch1_rx_en_label = bool(ch1_rx_en)
        self._ch1_rx_data_tcp_port_config = ConfigParser.ConfigParser()
        self._ch1_rx_data_tcp_port_config.read("Tyvak_GS.cfg")
        try: ch1_rx_data_tcp_port = self._ch1_rx_data_tcp_port_config.getint("rx", "ch1_port")
        except: ch1_rx_data_tcp_port = 4101
        self.ch1_rx_data_tcp_port = ch1_rx_data_tcp_port
        self.ch1_pwr = ch1_pwr = -130
        self.ch1_fft_range = ch1_fft_range = ch1_fft_range_config
        self.ch1_fft_max = ch1_fft_max = ch1_fft_max_config
        self._ch1_config_tcp_port_config = ConfigParser.ConfigParser()
        self._ch1_config_tcp_port_config.read(cfg_filename)
        try: ch1_config_tcp_port = self._ch1_config_tcp_port_config.getint("tx", "ch1_port")
        except: ch1_config_tcp_port = 4001
        self.ch1_config_tcp_port = ch1_config_tcp_port
        self.ch1_bt_label = ch1_bt_label = "{0}".format(ch1_bt)
        self.ch1_baud_label = ch1_baud_label = "{0}  ".format(ch1_baud)

        ##################################################
        # Blocks
        ##################################################
        self.tab_widget = Qt.QTabWidget()
        self.tab_widget_widget_0 = Qt.QWidget()
        self.tab_widget_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_widget_0)
        self.tab_widget_grid_layout_0 = Qt.QGridLayout()
        self.tab_widget_layout_0.addLayout(self.tab_widget_grid_layout_0)
        self.tab_widget.addTab(self.tab_widget_widget_0, "Water-rise")
        self.tab_widget_widget_1 = Qt.QWidget()
        self.tab_widget_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_widget_1)
        self.tab_widget_grid_layout_1 = Qt.QGridLayout()
        self.tab_widget_layout_1.addLayout(self.tab_widget_grid_layout_1)
        self.tab_widget.addTab(self.tab_widget_widget_1, "Threshold Config")
        self.tab_widget_widget_2 = Qt.QWidget()
        self.tab_widget_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tab_widget_widget_2)
        self.tab_widget_grid_layout_2 = Qt.QGridLayout()
        self.tab_widget_layout_2.addLayout(self.tab_widget_grid_layout_2)
        self.tab_widget.addTab(self.tab_widget_widget_2, "Channel FFT Config")
        self.top_grid_layout.addWidget(self.tab_widget, 5,0,6,6)
        self._water_range_range = Range(0, 200, 10, water_range_config, 200)
        self._water_range_win = RangeWidget(self._water_range_range, self.set_water_range, "Water-rise Range", "counter_slider", float)
        self.tab_widget_grid_layout_0.addWidget(self._water_range_win, 7,1)
        self._water_max_range = Range(-200, 50, 10, water_max_config, 200)
        self._water_max_win = RangeWidget(self._water_max_range, self.set_water_max, "Water-rise Max Intensity", "counter_slider", float)
        self.tab_widget_grid_layout_0.addWidget(self._water_max_win, 7,0)
        self._period_range = Range(1, 250, 1, 5, 200)
        self._period_win = RangeWidget(self._period_range, self.set_period, "period", "counter_slider", float)
        self.tab_widget_grid_layout_1.addWidget(self._period_win, 2,0,1,2)
        def _ch2_tx_freq_probe():
            while True:
                try:
                    val = self.ch2_probe_tx_freq.level()
                    self.set_ch2_tx_freq(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch2_tx_freq_thread = threading.Thread(target=_ch2_tx_freq_probe)
        _ch2_tx_freq_thread.daemon = True
        _ch2_tx_freq_thread.start()
        def _ch2_tx_corr_probe():
            while True:
                try:
                    val = self.ch2_probe_tx_corr.level()
                    self.set_ch2_tx_corr(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch2_tx_corr_thread = threading.Thread(target=_ch2_tx_corr_probe)
        _ch2_tx_corr_thread.daemon = True
        _ch2_tx_corr_thread.start()
        self._ch2_threshold_range = Range(-130, 0, 1, ch2_threshold_config, 200)
        self._ch2_threshold_win = RangeWidget(self._ch2_threshold_range, self.set_ch2_threshold, "Threshold", "counter_slider", float)
        self.tab_widget_grid_layout_1.addWidget(self._ch2_threshold_win, 0,1,1,1)
        def _ch2_rx_freq_probe():
            while True:
                try:
                    val = self.ch2_probe_rx_freq.level()
                    self.set_ch2_rx_freq(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch2_rx_freq_thread = threading.Thread(target=_ch2_rx_freq_probe)
        _ch2_rx_freq_thread.daemon = True
        _ch2_rx_freq_thread.start()
        def _ch2_rx_corr_probe():
            while True:
                try:
                    val = self.ch2_probe_rx_corr.level()
                    self.set_ch2_rx_corr(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch2_rx_corr_thread = threading.Thread(target=_ch2_rx_corr_probe)
        _ch2_rx_corr_thread.daemon = True
        _ch2_rx_corr_thread.start()
        def _ch2_pwr_probe():
            while True:
                try:
                    val = self.ch2_pwr_probe.level()
                    self.set_ch2_pwr(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1000.0))
        _ch2_pwr_thread = threading.Thread(target=_ch2_pwr_probe)
        _ch2_pwr_thread.daemon = True
        _ch2_pwr_thread.start()
        self._ch2_fft_range_range = Range(0, 200, 10, ch2_fft_range_config, 200)
        self._ch2_fft_range_win = RangeWidget(self._ch2_fft_range_range, self.set_ch2_fft_range, "Channel 2 FFT Range", "counter_slider", float)
        self.tab_widget_grid_layout_2.addWidget(self._ch2_fft_range_win, 1,1,1,1)
        self._ch2_fft_max_range = Range(-200, 50, 10, ch2_fft_max_config, 200)
        self._ch2_fft_max_win = RangeWidget(self._ch2_fft_max_range, self.set_ch2_fft_max, "Channel 2 FFT Max Intensity", "counter_slider", float)
        self.tab_widget_grid_layout_2.addWidget(self._ch2_fft_max_win, 0,1,1,1)
        def _ch1_tx_gain_probe():
            while True:
                try:
                    val = self.ch1_probe_tx_gain.level()
                    self.set_ch1_tx_gain(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch1_tx_gain_thread = threading.Thread(target=_ch1_tx_gain_probe)
        _ch1_tx_gain_thread.daemon = True
        _ch1_tx_gain_thread.start()
        def _ch1_tx_freq_probe():
            while True:
                try:
                    val = self.ch1_probe_tx_freq.level()
                    self.set_ch1_tx_freq(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch1_tx_freq_thread = threading.Thread(target=_ch1_tx_freq_probe)
        _ch1_tx_freq_thread.daemon = True
        _ch1_tx_freq_thread.start()
        def _ch1_tx_corr_probe():
            while True:
                try:
                    val = self.ch1_probe_tx_corr.level()
                    self.set_ch1_tx_corr(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch1_tx_corr_thread = threading.Thread(target=_ch1_tx_corr_probe)
        _ch1_tx_corr_thread.daemon = True
        _ch1_tx_corr_thread.start()
        self._ch1_threshold_range = Range(-130, 0, 1, ch1_threshold_config, 200)
        self._ch1_threshold_win = RangeWidget(self._ch1_threshold_range, self.set_ch1_threshold, "Threshold", "counter_slider", float)
        self.tab_widget_grid_layout_1.addWidget(self._ch1_threshold_win, 0,0,1,1)
        def _ch1_rx_gain_probe():
            while True:
                try:
                    val = self.ch1_probe_rx_gain.level()
                    self.set_ch1_rx_gain(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch1_rx_gain_thread = threading.Thread(target=_ch1_rx_gain_probe)
        _ch1_rx_gain_thread.daemon = True
        _ch1_rx_gain_thread.start()
        def _ch1_rx_freq_probe():
            while True:
                try:
                    val = self.ch1_probe_rx_freq.level()
                    self.set_ch1_rx_freq(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch1_rx_freq_thread = threading.Thread(target=_ch1_rx_freq_probe)
        _ch1_rx_freq_thread.daemon = True
        _ch1_rx_freq_thread.start()
        def _ch1_rx_corr_probe():
            while True:
                try:
                    val = self.ch1_probe_rx_corr.level()
                    self.set_ch1_rx_corr(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch1_rx_corr_thread = threading.Thread(target=_ch1_rx_corr_probe)
        _ch1_rx_corr_thread.daemon = True
        _ch1_rx_corr_thread.start()
        def _ch1_pwr_probe():
            while True:
                try:
                    val = self.ch1_pwr_probe.level()
                    self.set_ch1_pwr(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1000.0))
        _ch1_pwr_thread = threading.Thread(target=_ch1_pwr_probe)
        _ch1_pwr_thread.daemon = True
        _ch1_pwr_thread.start()
        self._ch1_fft_range_range = Range(0, 200, 10, ch1_fft_range_config, 200)
        self._ch1_fft_range_win = RangeWidget(self._ch1_fft_range_range, self.set_ch1_fft_range, "Channel 1 FFT Range", "counter_slider", float)
        self.tab_widget_grid_layout_2.addWidget(self._ch1_fft_range_win, 1,0,1,1)
        self._ch1_fft_max_range = Range(-200, 50, 10, ch1_fft_max_config, 200)
        self._ch1_fft_max_win = RangeWidget(self._ch1_fft_max_range, self.set_ch1_fft_max, "Channel 1 FFT Max Intensity", "counter_slider", float)
        self.tab_widget_grid_layout_2.addWidget(self._ch1_fft_max_win, 0,0,1,1)
        self._usrp_tx_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._usrp_tx_label_formatter = None
        else:
          self._usrp_tx_label_formatter = lambda x: x

        self._usrp_tx_label_tool_bar.addWidget(Qt.QLabel("USRP TX Center Freq"+": "))
        self._usrp_tx_label_label = Qt.QLabel(str(self._usrp_tx_label_formatter(self.usrp_tx_label)))
        self._usrp_tx_label_tool_bar.addWidget(self._usrp_tx_label_label)
        self.tab_widget_grid_layout_0.addWidget(self._usrp_tx_label_tool_bar, 8,0)

        self._usrp_rx_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._usrp_rx_label_formatter = None
        else:
          self._usrp_rx_label_formatter = lambda x: x

        self._usrp_rx_label_tool_bar.addWidget(Qt.QLabel("USRP RX Center Freq"+": "))
        self._usrp_rx_label_label = Qt.QLabel(str(self._usrp_rx_label_formatter(self.usrp_rx_label)))
        self._usrp_rx_label_tool_bar.addWidget(self._usrp_rx_label_label)
        self.tab_widget_grid_layout_0.addWidget(self._usrp_rx_label_tool_bar, 9,0)

        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join((usrp_addr, "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate * decm)
        self.uhd_usrp_source_0.set_center_freq(usrp_rx, 0)
        self.uhd_usrp_source_0.set_gain(ch1_rx_gain, 0)
        self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
        	",".join((usrp_addr, "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate * decm)
        self.uhd_usrp_sink_0_0.set_center_freq(usrp_tx, 0)
        self.uhd_usrp_sink_0_0.set_gain(ch1_tx_gain, 0)
        self.uhd_usrp_sink_0_0.set_antenna("TX/RX", 0)
        self.tyvak_transmit_buffer_pdu_0_0 = tyvak.transmit_buffer_pdu(1, ch2_baud, usrp_tx - (ch2_tx_freq +  ch2_tx_corr), ch2_pwr, ch2_threshold, 50)
        self.tyvak_transmit_buffer_pdu_0 = tyvak.transmit_buffer_pdu(1, ch1_baud, usrp_tx - (ch1_tx_freq +  ch1_tx_corr), ch1_pwr, ch1_threshold, 50)
        self.tx_tone_0_0 = tx_tone(
            f1=1209,
            f2=697,
        )
        self.tx_tone_0 = tx_tone(
            f1=1477,
            f2=941,
        )
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	512, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate *decm, #bw
        	"Water-rise Plot", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.1)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)

        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        colors = [6, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(water_max - water_range, water_max)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_widget_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win, 0,0,7,2)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	int(samp_rate), #size
        	samp_rate, #samp_rate
        	"", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-130, 0)

        self.qtgui_time_sink_x_0.set_y_label("Amplitude", "")

        self.qtgui_time_sink_x_0.enable_tags(-1, False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_NEG, ch1_threshold, 0.25, 1, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_control_panel(True)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ["Ch 1", "Ch 2", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tab_widget_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_win, 1,0,1,2)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
        	256, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"Channel 1", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.1)
        self.qtgui_freq_sink_x_0_0.set_y_axis(ch1_fft_max - ch1_fft_range, ch1_fft_max)
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)

        if not False:
          self.qtgui_freq_sink_x_0_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)

        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_win, 0,0,2,3)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	256, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"Channel 2", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.1)
        self.qtgui_freq_sink_x_0.set_y_axis(ch2_fft_max - ch2_fft_range, ch2_fft_max)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not False:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0,3,1,3)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate * decm, 2*ch1_baud, 1e3, firdes.WIN_HAMMING, 6.76))
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(decm, (firdes.low_pass(1.0, samp_rate, 2*ch1_baud, 2e3) ))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_ccc(1, (1, ), 0, samp_rate * decm)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(decm, (firdes.low_pass(1.0, samp_rate * decm, 2*ch2_baud, 1e3) ), (ch2_rx_freq +  ch2_rx_corr) - usrp_rx, samp_rate * decm)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(decm, (firdes.low_pass(1.0, samp_rate * decm, 2*ch1_baud, 1e3) ), (ch1_rx_freq +  ch1_rx_corr) - usrp_rx, samp_rate * decm)
        self.encode_mod_0 = encode_mod(
            baud=ch1_baud,
            bt=ch1_bt,
            samp_rate=samp_rate,
        )
        self.demod_decode_0_0 = demod_decode(
            baud=ch2_baud,
            samp_rate=samp_rate,
        )
        self.demod_decode_0 = demod_decode(
            baud=ch1_baud,
            samp_rate=samp_rate,
        )
        self._ch2_tx_freq_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch2_tx_freq_label_formatter = None
        else:
          self._ch2_tx_freq_label_formatter = lambda x: x

        self._ch2_tx_freq_label_tool_bar.addWidget(Qt.QLabel("TX Freq"+": "))
        self._ch2_tx_freq_label_label = Qt.QLabel(str(self._ch2_tx_freq_label_formatter(self.ch2_tx_freq_label)))
        self._ch2_tx_freq_label_tool_bar.addWidget(self._ch2_tx_freq_label_label)
        self.top_grid_layout.addWidget(self._ch2_tx_freq_label_tool_bar, 2,3,1,1)

        self._ch2_tx_en_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch2_tx_en_label_formatter = None
        else:
          self._ch2_tx_en_label_formatter = lambda x: x

        self._ch2_tx_en_label_tool_bar.addWidget(Qt.QLabel("TX Enabled"+": "))
        self._ch2_tx_en_label_label = Qt.QLabel(str(self._ch2_tx_en_label_formatter(self.ch2_tx_en_label)))
        self._ch2_tx_en_label_tool_bar.addWidget(self._ch2_tx_en_label_label)
        self.top_grid_layout.addWidget(self._ch2_tx_en_label_tool_bar, 2,5,1,1)

        self._ch2_rx_freq_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch2_rx_freq_label_formatter = None
        else:
          self._ch2_rx_freq_label_formatter = lambda x: x

        self._ch2_rx_freq_label_tool_bar.addWidget(Qt.QLabel("RX Freq"+": "))
        self._ch2_rx_freq_label_label = Qt.QLabel(str(self._ch2_rx_freq_label_formatter(self.ch2_rx_freq_label)))
        self._ch2_rx_freq_label_tool_bar.addWidget(self._ch2_rx_freq_label_label)
        self.top_grid_layout.addWidget(self._ch2_rx_freq_label_tool_bar, 3,3,1,1)

        self._ch2_rx_en_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch2_rx_en_label_formatter = None
        else:
          self._ch2_rx_en_label_formatter = lambda x: x

        self._ch2_rx_en_label_tool_bar.addWidget(Qt.QLabel("RX Enabled"+": "))
        self._ch2_rx_en_label_label = Qt.QLabel(str(self._ch2_rx_en_label_formatter(self.ch2_rx_en_label)))
        self._ch2_rx_en_label_tool_bar.addWidget(self._ch2_rx_en_label_label)
        self.top_grid_layout.addWidget(self._ch2_rx_en_label_tool_bar, 3,5,1,1)

        self.ch2_pwr_probe = blocks.probe_signal_f()
        def _ch2_h_raw_probe():
            while True:
                try:
                    val = self.ch2_probe_h.level()
                    self.set_ch2_h_raw(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch2_h_raw_thread = threading.Thread(target=_ch2_h_raw_probe)
        _ch2_h_raw_thread.daemon = True
        _ch2_h_raw_thread.start()
        self._ch2_bt_label_0_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch2_bt_label_0_formatter = None
        else:
          self._ch2_bt_label_0_formatter = lambda x: x

        self._ch2_bt_label_0_tool_bar.addWidget(Qt.QLabel("H"+": "))
        self._ch2_bt_label_0_label = Qt.QLabel(str(self._ch2_bt_label_0_formatter(self.ch2_bt_label_0)))
        self._ch2_bt_label_0_tool_bar.addWidget(self._ch2_bt_label_0_label)
        self.top_grid_layout.addWidget(self._ch2_bt_label_0_tool_bar, 3,4,1,1)

        def _ch2_baud_raw_probe():
            while True:
                try:
                    val = self.ch2_probe_baud.level()
                    self.set_ch2_baud_raw(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch2_baud_raw_thread = threading.Thread(target=_ch2_baud_raw_probe)
        _ch2_baud_raw_thread.daemon = True
        _ch2_baud_raw_thread.start()
        self._ch2_baud_label_0_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch2_baud_label_0_formatter = None
        else:
          self._ch2_baud_label_0_formatter = lambda x: x

        self._ch2_baud_label_0_tool_bar.addWidget(Qt.QLabel("Baud"+": "))
        self._ch2_baud_label_0_label = Qt.QLabel(str(self._ch2_baud_label_0_formatter(self.ch2_baud_label_0)))
        self._ch2_baud_label_0_tool_bar.addWidget(self._ch2_baud_label_0_label)
        self.top_grid_layout.addWidget(self._ch2_baud_label_0_tool_bar, 2,4,1,1)

        self._ch1_tx_gain_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch1_tx_gain_label_formatter = None
        else:
          self._ch1_tx_gain_label_formatter = lambda x: x

        self._ch1_tx_gain_label_tool_bar.addWidget(Qt.QLabel("TX Gain"+": "))
        self._ch1_tx_gain_label_label = Qt.QLabel(str(self._ch1_tx_gain_label_formatter(self.ch1_tx_gain_label)))
        self._ch1_tx_gain_label_tool_bar.addWidget(self._ch1_tx_gain_label_label)
        self.tab_widget_grid_layout_0.addWidget(self._ch1_tx_gain_label_tool_bar, 8,1)

        self._ch1_tx_freq_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch1_tx_freq_label_formatter = None
        else:
          self._ch1_tx_freq_label_formatter = lambda x: x

        self._ch1_tx_freq_label_tool_bar.addWidget(Qt.QLabel("TX Freq"+": "))
        self._ch1_tx_freq_label_label = Qt.QLabel(str(self._ch1_tx_freq_label_formatter(self.ch1_tx_freq_label)))
        self._ch1_tx_freq_label_tool_bar.addWidget(self._ch1_tx_freq_label_label)
        self.top_grid_layout.addWidget(self._ch1_tx_freq_label_tool_bar, 2,0,1,1)

        self._ch1_tx_en_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch1_tx_en_label_formatter = None
        else:
          self._ch1_tx_en_label_formatter = lambda x: x

        self._ch1_tx_en_label_tool_bar.addWidget(Qt.QLabel("TX Enabled"+": "))
        self._ch1_tx_en_label_label = Qt.QLabel(str(self._ch1_tx_en_label_formatter(self.ch1_tx_en_label)))
        self._ch1_tx_en_label_tool_bar.addWidget(self._ch1_tx_en_label_label)
        self.top_grid_layout.addWidget(self._ch1_tx_en_label_tool_bar, 2,2,1,1)

        self._ch1_rx_gain_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch1_rx_gain_label_formatter = None
        else:
          self._ch1_rx_gain_label_formatter = lambda x: x

        self._ch1_rx_gain_label_tool_bar.addWidget(Qt.QLabel("RX Gain"+": "))
        self._ch1_rx_gain_label_label = Qt.QLabel(str(self._ch1_rx_gain_label_formatter(self.ch1_rx_gain_label)))
        self._ch1_rx_gain_label_tool_bar.addWidget(self._ch1_rx_gain_label_label)
        self.tab_widget_grid_layout_0.addWidget(self._ch1_rx_gain_label_tool_bar, 9,1)

        self._ch1_rx_freq_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch1_rx_freq_label_formatter = None
        else:
          self._ch1_rx_freq_label_formatter = lambda x: x

        self._ch1_rx_freq_label_tool_bar.addWidget(Qt.QLabel("RX Freq"+": "))
        self._ch1_rx_freq_label_label = Qt.QLabel(str(self._ch1_rx_freq_label_formatter(self.ch1_rx_freq_label)))
        self._ch1_rx_freq_label_tool_bar.addWidget(self._ch1_rx_freq_label_label)
        self.top_grid_layout.addWidget(self._ch1_rx_freq_label_tool_bar, 3,0,1,1)

        self._ch1_rx_en_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch1_rx_en_label_formatter = None
        else:
          self._ch1_rx_en_label_formatter = lambda x: x

        self._ch1_rx_en_label_tool_bar.addWidget(Qt.QLabel("RX Enabled"+": "))
        self._ch1_rx_en_label_label = Qt.QLabel(str(self._ch1_rx_en_label_formatter(self.ch1_rx_en_label)))
        self._ch1_rx_en_label_tool_bar.addWidget(self._ch1_rx_en_label_label)
        self.top_grid_layout.addWidget(self._ch1_rx_en_label_tool_bar, 3,2,1,1)

        self.ch1_pwr_probe = blocks.probe_signal_f()
        def _ch1_h_raw_probe():
            while True:
                try:
                    val = self.ch1_probe_h.level()
                    self.set_ch1_h_raw(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch1_h_raw_thread = threading.Thread(target=_ch1_h_raw_probe)
        _ch1_h_raw_thread.daemon = True
        _ch1_h_raw_thread.start()
        self._ch1_bt_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch1_bt_label_formatter = None
        else:
          self._ch1_bt_label_formatter = lambda x: x

        self._ch1_bt_label_tool_bar.addWidget(Qt.QLabel("H"+": "))
        self._ch1_bt_label_label = Qt.QLabel(str(self._ch1_bt_label_formatter(self.ch1_bt_label)))
        self._ch1_bt_label_tool_bar.addWidget(self._ch1_bt_label_label)
        self.top_grid_layout.addWidget(self._ch1_bt_label_tool_bar, 3,1,1,1)

        def _ch1_baud_raw_probe():
            while True:
                try:
                    val = self.ch1_probe_baud.level()
                    self.set_ch1_baud_raw(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1))
        _ch1_baud_raw_thread = threading.Thread(target=_ch1_baud_raw_probe)
        _ch1_baud_raw_thread.daemon = True
        _ch1_baud_raw_thread.start()
        self._ch1_baud_label_tool_bar = Qt.QToolBar(self)

        if None:
          self._ch1_baud_label_formatter = None
        else:
          self._ch1_baud_label_formatter = lambda x: x

        self._ch1_baud_label_tool_bar.addWidget(Qt.QLabel("Baud"+": "))
        self._ch1_baud_label_label = Qt.QLabel(str(self._ch1_baud_label_formatter(self.ch1_baud_label)))
        self._ch1_baud_label_tool_bar.addWidget(self._ch1_baud_label_label)
        self.top_grid_layout.addWidget(self._ch1_baud_label_tool_bar, 2,1,1,1)

        self.blocks_socket_pdu_0_0_0_0 = blocks.socket_pdu("TCP_SERVER", config_tcp_ip, str(ch2_config_tcp_port), 10000, False)
        self.blocks_socket_pdu_0_0_0 = blocks.socket_pdu("TCP_SERVER", config_tcp_ip, str(ch1_config_tcp_port), 10000, False)
        self.blocks_socket_pdu_0_0 = blocks.socket_pdu("TCP_SERVER", rx_data_tcp_ip, str(ch2_rx_data_tcp_port), 10000, False)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", rx_data_tcp_ip, str(ch1_rx_data_tcp_port), 10000, False)
        self.approx_power_0_0 = approx_power(
            averages=int(samp_rate / (1000.0/period)),
        )
        self.approx_power_0 = approx_power(
            averages=int(samp_rate / (1000.0/period)),
        )

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0_0_0, 'pdus'), (self.tyvak_transmit_buffer_pdu_0, 'in'))
        self.msg_connect((self.blocks_socket_pdu_0_0_0_0, 'pdus'), (self.tyvak_transmit_buffer_pdu_0_0, 'in'))
        self.msg_connect((self.demod_decode_0, 'out'), (self.blocks_socket_pdu_0, 'pdus'))
        self.msg_connect((self.demod_decode_0_0, 'out'), (self.blocks_socket_pdu_0_0, 'pdus'))
        self.msg_connect((self.tyvak_transmit_buffer_pdu_0, 'out'), (self.encode_mod_0, 'in'))
        self.msg_connect((self.tyvak_transmit_buffer_pdu_0, 'freq'), (self.freq_xlating_fir_filter_xxx_1, 'freq'))
        self.msg_connect((self.tyvak_transmit_buffer_pdu_0, 'out'), (self.tx_tone_0, 'in'))
        self.msg_connect((self.tyvak_transmit_buffer_pdu_0_0, 'out'), (self.encode_mod_0, 'in'))
        self.msg_connect((self.tyvak_transmit_buffer_pdu_0_0, 'freq'), (self.freq_xlating_fir_filter_xxx_1, 'freq'))
        self.msg_connect((self.tyvak_transmit_buffer_pdu_0_0, 'out'), (self.tx_tone_0_0, 'in'))
        self.connect((self.approx_power_0, 0), (self.ch1_pwr_probe, 0))
        self.connect((self.approx_power_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.approx_power_0_0, 0), (self.ch2_pwr_probe, 0))
        self.connect((self.approx_power_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.encode_mod_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.approx_power_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.demod_decode_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.approx_power_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.demod_decode_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.freq_xlating_fir_filter_xxx_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Tyvak_GS")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()


    def get_decm(self):
        return self.decm

    def set_decm(self, decm):
        self.decm = decm
        self.set_ch2_rx_en(int((self.ch2_rx_freq > 0) and (self.rx_delta_abs < (self.samp_rate*self.decm))))
        self.set_ch2_tx_en(int((self.ch2_tx_freq > 0) and (self.tx_delta_abs < (self.samp_rate*self.decm))))
        self.set_samp_rate(403.225806451613e3 / self.decm)
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((firdes.low_pass(1.0, self.samp_rate * self.decm, 2*self.ch2_baud, 1e3) ))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate * self.decm, 2*self.ch1_baud, 1e3, firdes.WIN_HAMMING, 6.76))
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate * self.decm)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate * self.decm)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate *self.decm)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1.0, self.samp_rate * self.decm, 2*self.ch1_baud, 1e3) ))

    def get_ch2_tx_freq(self):
        return self.ch2_tx_freq

    def set_ch2_tx_freq(self, ch2_tx_freq):
        self.ch2_tx_freq = ch2_tx_freq
        self.set_ch2_tx_en(int((self.ch2_tx_freq > 0) and (self.tx_delta_abs < (self.samp_rate*self.decm))))
        self.set_ch2_tx_freq_label(self._ch2_tx_freq_label_formatter("{:3.4f} MHz  ".format((self.ch2_tx_freq+self.ch2_tx_corr) / 1e6)))
        self.set_tx_delta_abs(abs(self.ch1_tx_freq - self.ch2_tx_freq))
        self.set_usrp_tx((self.ch1_tx_freq*self.ch1_tx_en + self.ch2_tx_freq*self.ch2_tx_en) / max(1, (self.ch1_tx_en + self.ch2_tx_en)))
        self.tyvak_transmit_buffer_pdu_0_0.set_freq_offset(self.usrp_tx - (self.ch2_tx_freq +  self.ch2_tx_corr))

    def get_ch2_rx_freq(self):
        return self.ch2_rx_freq

    def set_ch2_rx_freq(self, ch2_rx_freq):
        self.ch2_rx_freq = ch2_rx_freq
        self.set_ch2_rx_en(int((self.ch2_rx_freq > 0) and (self.rx_delta_abs < (self.samp_rate*self.decm))))
        self.set_ch2_rx_freq_label(self._ch2_rx_freq_label_formatter("{:3.4f} MHz  ".format((self.ch2_rx_freq+self.ch2_rx_corr) / 1e6)))
        self.set_rx_delta_abs(abs(self.ch1_rx_freq - self.ch2_rx_freq))
        self.set_usrp_rx((self.ch1_rx_freq*self.ch1_rx_en + self.ch2_rx_freq*self.ch2_rx_en) / max(1, (self.ch1_rx_en + self.ch2_rx_en)))
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq((self.ch2_rx_freq +  self.ch2_rx_corr) - self.usrp_rx)

    def get_ch1_tx_freq(self):
        return self.ch1_tx_freq

    def set_ch1_tx_freq(self, ch1_tx_freq):
        self.ch1_tx_freq = ch1_tx_freq
        self.set_ch1_tx_en(int(self.ch1_tx_freq > 0))
        self.set_ch1_tx_freq_label(self._ch1_tx_freq_label_formatter("{:3.4f} MHz  ".format((self.ch1_tx_freq+self.ch1_tx_corr) / 1e6)))
        self.set_tx_delta_abs(abs(self.ch1_tx_freq - self.ch2_tx_freq))
        self.set_usrp_tx((self.ch1_tx_freq*self.ch1_tx_en + self.ch2_tx_freq*self.ch2_tx_en) / max(1, (self.ch1_tx_en + self.ch2_tx_en)))
        self.tyvak_transmit_buffer_pdu_0.set_freq_offset(self.usrp_tx - (self.ch1_tx_freq +  self.ch1_tx_corr))

    def get_ch1_rx_freq(self):
        return self.ch1_rx_freq

    def set_ch1_rx_freq(self, ch1_rx_freq):
        self.ch1_rx_freq = ch1_rx_freq
        self.set_ch1_rx_en(int(self.ch1_rx_freq > 0))
        self.set_ch1_rx_freq_label(self._ch1_rx_freq_label_formatter("{:3.4f} MHz  ".format((self.ch1_rx_freq+self.ch1_rx_corr) / 1e6)))
        self.set_rx_delta_abs(abs(self.ch1_rx_freq - self.ch2_rx_freq))
        self.set_usrp_rx((self.ch1_rx_freq*self.ch1_rx_en + self.ch2_rx_freq*self.ch2_rx_en) / max(1, (self.ch1_rx_en + self.ch2_rx_en)))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((self.ch1_rx_freq +  self.ch1_rx_corr) - self.usrp_rx)

    def get_tx_delta_abs(self):
        return self.tx_delta_abs

    def set_tx_delta_abs(self, tx_delta_abs):
        self.tx_delta_abs = tx_delta_abs
        self.set_ch2_tx_en(int((self.ch2_tx_freq > 0) and (self.tx_delta_abs < (self.samp_rate*self.decm))))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_ch2_rx_en(int((self.ch2_rx_freq > 0) and (self.rx_delta_abs < (self.samp_rate*self.decm))))
        self.set_ch2_tx_en(int((self.ch2_tx_freq > 0) and (self.tx_delta_abs < (self.samp_rate*self.decm))))
        self.approx_power_0_0.set_averages(int(self.samp_rate / (1000.0/self.period)))
        self.demod_decode_0_0.set_samp_rate(self.samp_rate)
        self.encode_mod_0.set_samp_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((firdes.low_pass(1.0, self.samp_rate * self.decm, 2*self.ch2_baud, 1e3) ))
        self.interp_fir_filter_xxx_0.set_taps((firdes.low_pass(1.0, self.samp_rate, 2*self.ch1_baud, 2e3) ))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate * self.decm, 2*self.ch1_baud, 1e3, firdes.WIN_HAMMING, 6.76))
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate * self.decm)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate * self.decm)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate *self.decm)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.approx_power_0.set_averages(int(self.samp_rate / (1000.0/self.period)))
        self.demod_decode_0.set_samp_rate(self.samp_rate)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1.0, self.samp_rate * self.decm, 2*self.ch1_baud, 1e3) ))
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_rx_delta_abs(self):
        return self.rx_delta_abs

    def set_rx_delta_abs(self, rx_delta_abs):
        self.rx_delta_abs = rx_delta_abs
        self.set_ch2_rx_en(int((self.ch2_rx_freq > 0) and (self.rx_delta_abs < (self.samp_rate*self.decm))))

    def get_ch2_tx_en(self):
        return self.ch2_tx_en

    def set_ch2_tx_en(self, ch2_tx_en):
        self.ch2_tx_en = ch2_tx_en
        self.set_ch2_tx_en_label(self._ch2_tx_en_label_formatter(bool(self.ch2_tx_en)))
        self.set_usrp_tx((self.ch1_tx_freq*self.ch1_tx_en + self.ch2_tx_freq*self.ch2_tx_en) / max(1, (self.ch1_tx_en + self.ch2_tx_en)))

    def get_ch2_rx_en(self):
        return self.ch2_rx_en

    def set_ch2_rx_en(self, ch2_rx_en):
        self.ch2_rx_en = ch2_rx_en
        self.set_ch2_rx_en_label(self._ch2_rx_en_label_formatter(bool(self.ch2_rx_en)))
        self.set_usrp_rx((self.ch1_rx_freq*self.ch1_rx_en + self.ch2_rx_freq*self.ch2_rx_en) / max(1, (self.ch1_rx_en + self.ch2_rx_en)))

    def get_ch2_h_raw(self):
        return self.ch2_h_raw

    def set_ch2_h_raw(self, ch2_h_raw):
        self.ch2_h_raw = ch2_h_raw
        self.set_ch2_bt(max(0.01, self.ch2_h_raw / 100.0))

    def get_ch2_baud_raw(self):
        return self.ch2_baud_raw

    def set_ch2_baud_raw(self, ch2_baud_raw):
        self.ch2_baud_raw = ch2_baud_raw
        self.set_ch2_baud(max(9600, self.ch2_baud_raw))

    def get_ch1_tx_en(self):
        return self.ch1_tx_en

    def set_ch1_tx_en(self, ch1_tx_en):
        self.ch1_tx_en = ch1_tx_en
        self.set_ch1_tx_en_label(self._ch1_tx_en_label_formatter(bool(self.ch1_tx_en)))
        self.set_usrp_tx((self.ch1_tx_freq*self.ch1_tx_en + self.ch2_tx_freq*self.ch2_tx_en) / max(1, (self.ch1_tx_en + self.ch2_tx_en)))

    def get_ch1_rx_en(self):
        return self.ch1_rx_en

    def set_ch1_rx_en(self, ch1_rx_en):
        self.ch1_rx_en = ch1_rx_en
        self.set_ch1_rx_en_label(self._ch1_rx_en_label_formatter(bool(self.ch1_rx_en)))
        self.set_usrp_rx((self.ch1_rx_freq*self.ch1_rx_en + self.ch2_rx_freq*self.ch2_rx_en) / max(1, (self.ch1_rx_en + self.ch2_rx_en)))

    def get_ch1_h_raw(self):
        return self.ch1_h_raw

    def set_ch1_h_raw(self, ch1_h_raw):
        self.ch1_h_raw = ch1_h_raw
        self.set_ch1_bt(max(0.01, self.ch1_h_raw / 100.0))

    def get_ch1_baud_raw(self):
        return self.ch1_baud_raw

    def set_ch1_baud_raw(self, ch1_baud_raw):
        self.ch1_baud_raw = ch1_baud_raw
        self.set_ch1_baud(max(9600, self.ch1_baud_raw))

    def get_cfg_filename(self):
        return self.cfg_filename

    def set_cfg_filename(self, cfg_filename):
        self.cfg_filename = cfg_filename
        self._ch1_config_tcp_port_config = ConfigParser.ConfigParser()
        self._ch1_config_tcp_port_config.read(self.cfg_filename)
        if not self._ch1_config_tcp_port_config.has_section("tx"):
        	self._ch1_config_tcp_port_config.add_section("tx")
        self._ch1_config_tcp_port_config.set("tx", "ch1_port", str(None))
        self._ch1_config_tcp_port_config.write(open(self.cfg_filename, 'w'))
        self._ch1_fft_max_config_config = ConfigParser.ConfigParser()
        self._ch1_fft_max_config_config.read(self.cfg_filename)
        if not self._ch1_fft_max_config_config.has_section("settings"):
        	self._ch1_fft_max_config_config.add_section("settings")
        self._ch1_fft_max_config_config.set("settings", "ch1_fft_max", str(self.ch1_fft_max))
        self._ch1_fft_max_config_config.write(open(self.cfg_filename, 'w'))
        self._ch1_fft_range_config_config = ConfigParser.ConfigParser()
        self._ch1_fft_range_config_config.read(self.cfg_filename)
        if not self._ch1_fft_range_config_config.has_section("settings"):
        	self._ch1_fft_range_config_config.add_section("settings")
        self._ch1_fft_range_config_config.set("settings", "ch1_fft_range", str(self.ch1_fft_range))
        self._ch1_fft_range_config_config.write(open(self.cfg_filename, 'w'))
        self._ch1_threshold_config_config = ConfigParser.ConfigParser()
        self._ch1_threshold_config_config.read(self.cfg_filename)
        if not self._ch1_threshold_config_config.has_section("settings"):
        	self._ch1_threshold_config_config.add_section("settings")
        self._ch1_threshold_config_config.set("settings", "ch1_threshold", str(self.ch1_threshold))
        self._ch1_threshold_config_config.write(open(self.cfg_filename, 'w'))
        self._ch2_config_tcp_port_config = ConfigParser.ConfigParser()
        self._ch2_config_tcp_port_config.read(self.cfg_filename)
        if not self._ch2_config_tcp_port_config.has_section("tx"):
        	self._ch2_config_tcp_port_config.add_section("tx")
        self._ch2_config_tcp_port_config.set("tx", "ch2_port", str(None))
        self._ch2_config_tcp_port_config.write(open(self.cfg_filename, 'w'))
        self._ch2_fft_max_config_config = ConfigParser.ConfigParser()
        self._ch2_fft_max_config_config.read(self.cfg_filename)
        if not self._ch2_fft_max_config_config.has_section("settings"):
        	self._ch2_fft_max_config_config.add_section("settings")
        self._ch2_fft_max_config_config.set("settings", "ch2_fft_max", str(self.ch2_fft_max))
        self._ch2_fft_max_config_config.write(open(self.cfg_filename, 'w'))
        self._ch2_fft_range_config_config = ConfigParser.ConfigParser()
        self._ch2_fft_range_config_config.read(self.cfg_filename)
        if not self._ch2_fft_range_config_config.has_section("settings"):
        	self._ch2_fft_range_config_config.add_section("settings")
        self._ch2_fft_range_config_config.set("settings", "ch2_fft_range", str(self.ch2_fft_range))
        self._ch2_fft_range_config_config.write(open(self.cfg_filename, 'w'))
        self._ch2_threshold_config_config = ConfigParser.ConfigParser()
        self._ch2_threshold_config_config.read(self.cfg_filename)
        if not self._ch2_threshold_config_config.has_section("settings"):
        	self._ch2_threshold_config_config.add_section("settings")
        self._ch2_threshold_config_config.set("settings", "ch2_threshold", str(self.ch2_threshold))
        self._ch2_threshold_config_config.write(open(self.cfg_filename, 'w'))
        self._config_tcp_ip_config = ConfigParser.ConfigParser()
        self._config_tcp_ip_config.read(self.cfg_filename)
        if not self._config_tcp_ip_config.has_section("tx"):
        	self._config_tcp_ip_config.add_section("tx")
        self._config_tcp_ip_config.set("tx", "ip", str(None))
        self._config_tcp_ip_config.write(open(self.cfg_filename, 'w'))
        self._period_config_config = ConfigParser.ConfigParser()
        self._period_config_config.read(self.cfg_filename)
        if not self._period_config_config.has_section("settings"):
        	self._period_config_config.add_section("settings")
        self._period_config_config.set("settings", "period", str(self.period))
        self._period_config_config.write(open(self.cfg_filename, 'w'))
        self._usrp_addr_config = ConfigParser.ConfigParser()
        self._usrp_addr_config.read(self.cfg_filename)
        if not self._usrp_addr_config.has_section("usrp"):
        	self._usrp_addr_config.add_section("usrp")
        self._usrp_addr_config.set("usrp", "addr", str(None))
        self._usrp_addr_config.write(open(self.cfg_filename, 'w'))
        self._water_max_config_config = ConfigParser.ConfigParser()
        self._water_max_config_config.read(self.cfg_filename)
        if not self._water_max_config_config.has_section("settings"):
        	self._water_max_config_config.add_section("settings")
        self._water_max_config_config.set("settings", "water_max", str(self.water_max))
        self._water_max_config_config.write(open(self.cfg_filename, 'w'))
        self._water_range_config_config = ConfigParser.ConfigParser()
        self._water_range_config_config.read(self.cfg_filename)
        if not self._water_range_config_config.has_section("settings"):
        	self._water_range_config_config.add_section("settings")
        self._water_range_config_config.set("settings", "water_range", str(self.water_range))
        self._water_range_config_config.write(open(self.cfg_filename, 'w'))

    def get_water_range_config(self):
        return self.water_range_config

    def set_water_range_config(self, water_range_config):
        self.water_range_config = water_range_config
        self.set_water_range(self.water_range_config)

    def get_water_max_config(self):
        return self.water_max_config

    def set_water_max_config(self, water_max_config):
        self.water_max_config = water_max_config
        self.set_water_max(self.water_max_config)

    def get_usrp_tx(self):
        return self.usrp_tx

    def set_usrp_tx(self, usrp_tx):
        self.usrp_tx = usrp_tx
        self.set_usrp_tx_label(self._usrp_tx_label_formatter("{:3.4f} MHz  ".format(self.usrp_tx / 1e6)))
        self.tyvak_transmit_buffer_pdu_0.set_freq_offset(self.usrp_tx - (self.ch1_tx_freq +  self.ch1_tx_corr))
        self.tyvak_transmit_buffer_pdu_0_0.set_freq_offset(self.usrp_tx - (self.ch2_tx_freq +  self.ch2_tx_corr))
        self.uhd_usrp_sink_0_0.set_center_freq(self.usrp_tx, 0)

    def get_usrp_rx(self):
        return self.usrp_rx

    def set_usrp_rx(self, usrp_rx):
        self.usrp_rx = usrp_rx
        self.set_usrp_rx_label(self._usrp_rx_label_formatter("{:3.4f} MHz  ".format(self.usrp_rx / 1e6)))
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq((self.ch2_rx_freq +  self.ch2_rx_corr) - self.usrp_rx)
        self.uhd_usrp_source_0.set_center_freq(self.usrp_rx, 0)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((self.ch1_rx_freq +  self.ch1_rx_corr) - self.usrp_rx)

    def get_ch2_tx_corr(self):
        return self.ch2_tx_corr

    def set_ch2_tx_corr(self, ch2_tx_corr):
        self.ch2_tx_corr = ch2_tx_corr
        self.set_ch2_tx_freq_label(self._ch2_tx_freq_label_formatter("{:3.4f} MHz  ".format((self.ch2_tx_freq+self.ch2_tx_corr) / 1e6)))
        self.tyvak_transmit_buffer_pdu_0_0.set_freq_offset(self.usrp_tx - (self.ch2_tx_freq +  self.ch2_tx_corr))

    def get_ch2_threshold_config(self):
        return self.ch2_threshold_config

    def set_ch2_threshold_config(self, ch2_threshold_config):
        self.ch2_threshold_config = ch2_threshold_config
        self.set_ch2_threshold(self.ch2_threshold_config)

    def get_ch2_rx_corr(self):
        return self.ch2_rx_corr

    def set_ch2_rx_corr(self, ch2_rx_corr):
        self.ch2_rx_corr = ch2_rx_corr
        self.set_ch2_rx_freq_label(self._ch2_rx_freq_label_formatter("{:3.4f} MHz  ".format((self.ch2_rx_freq+self.ch2_rx_corr) / 1e6)))
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq((self.ch2_rx_freq +  self.ch2_rx_corr) - self.usrp_rx)

    def get_ch2_fft_range_config(self):
        return self.ch2_fft_range_config

    def set_ch2_fft_range_config(self, ch2_fft_range_config):
        self.ch2_fft_range_config = ch2_fft_range_config
        self.set_ch2_fft_range(self.ch2_fft_range_config)

    def get_ch2_fft_max_config(self):
        return self.ch2_fft_max_config

    def set_ch2_fft_max_config(self, ch2_fft_max_config):
        self.ch2_fft_max_config = ch2_fft_max_config
        self.set_ch2_fft_max(self.ch2_fft_max_config)

    def get_ch2_bt(self):
        return self.ch2_bt

    def set_ch2_bt(self, ch2_bt):
        self.ch2_bt = ch2_bt
        self.set_ch2_bt_label_0(self._ch2_bt_label_0_formatter("{0}".format(self.ch2_bt)))

    def get_ch2_baud(self):
        return self.ch2_baud

    def set_ch2_baud(self, ch2_baud):
        self.ch2_baud = ch2_baud
        self.set_ch2_baud_label_0(self._ch2_baud_label_0_formatter("{0}  ".format(self.ch2_baud)))
        self.demod_decode_0_0.set_baud(self.ch2_baud)
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((firdes.low_pass(1.0, self.samp_rate * self.decm, 2*self.ch2_baud, 1e3) ))
        self.tyvak_transmit_buffer_pdu_0_0.set_baud(self.ch2_baud)

    def get_ch1_tx_gain(self):
        return self.ch1_tx_gain

    def set_ch1_tx_gain(self, ch1_tx_gain):
        self.ch1_tx_gain = ch1_tx_gain
        self.set_ch1_tx_gain_label(self._ch1_tx_gain_label_formatter("{0:2.0f} dB  ".format(self.ch1_tx_gain)))
        self.uhd_usrp_sink_0_0.set_gain(self.ch1_tx_gain, 0)


    def get_ch1_tx_corr(self):
        return self.ch1_tx_corr

    def set_ch1_tx_corr(self, ch1_tx_corr):
        self.ch1_tx_corr = ch1_tx_corr
        self.set_ch1_tx_freq_label(self._ch1_tx_freq_label_formatter("{:3.4f} MHz  ".format((self.ch1_tx_freq+self.ch1_tx_corr) / 1e6)))
        self.tyvak_transmit_buffer_pdu_0.set_freq_offset(self.usrp_tx - (self.ch1_tx_freq +  self.ch1_tx_corr))

    def get_ch1_threshold_config(self):
        return self.ch1_threshold_config

    def set_ch1_threshold_config(self, ch1_threshold_config):
        self.ch1_threshold_config = ch1_threshold_config
        self.set_ch1_threshold(self.ch1_threshold_config)

    def get_ch1_rx_gain(self):
        return self.ch1_rx_gain

    def set_ch1_rx_gain(self, ch1_rx_gain):
        self.ch1_rx_gain = ch1_rx_gain
        self.set_ch1_rx_gain_label(self._ch1_rx_gain_label_formatter("{0:2.0f} dB  ".format(self.ch1_rx_gain)))
        self.uhd_usrp_source_0.set_gain(self.ch1_rx_gain, 0)


    def get_ch1_rx_corr(self):
        return self.ch1_rx_corr

    def set_ch1_rx_corr(self, ch1_rx_corr):
        self.ch1_rx_corr = ch1_rx_corr
        self.set_ch1_rx_freq_label(self._ch1_rx_freq_label_formatter("{:3.4f} MHz  ".format((self.ch1_rx_freq+self.ch1_rx_corr) / 1e6)))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq((self.ch1_rx_freq +  self.ch1_rx_corr) - self.usrp_rx)

    def get_ch1_fft_range_config(self):
        return self.ch1_fft_range_config

    def set_ch1_fft_range_config(self, ch1_fft_range_config):
        self.ch1_fft_range_config = ch1_fft_range_config
        self.set_ch1_fft_range(self.ch1_fft_range_config)

    def get_ch1_fft_max_config(self):
        return self.ch1_fft_max_config

    def set_ch1_fft_max_config(self, ch1_fft_max_config):
        self.ch1_fft_max_config = ch1_fft_max_config
        self.set_ch1_fft_max(self.ch1_fft_max_config)

    def get_ch1_bt(self):
        return self.ch1_bt

    def set_ch1_bt(self, ch1_bt):
        self.ch1_bt = ch1_bt
        self.set_ch1_bt_label(self._ch1_bt_label_formatter("{0}".format(self.ch1_bt)))
        self.encode_mod_0.set_bt(self.ch1_bt)

    def get_ch1_baud(self):
        return self.ch1_baud

    def set_ch1_baud(self, ch1_baud):
        self.ch1_baud = ch1_baud
        self.set_ch1_baud_label(self._ch1_baud_label_formatter("{0}  ".format(self.ch1_baud)))
        self.encode_mod_0.set_baud(self.ch1_baud)
        self.interp_fir_filter_xxx_0.set_taps((firdes.low_pass(1.0, self.samp_rate, 2*self.ch1_baud, 2e3) ))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate * self.decm, 2*self.ch1_baud, 1e3, firdes.WIN_HAMMING, 6.76))
        self.tyvak_transmit_buffer_pdu_0.set_baud(self.ch1_baud)
        self.demod_decode_0.set_baud(self.ch1_baud)
        self.freq_xlating_fir_filter_xxx_0.set_taps((firdes.low_pass(1.0, self.samp_rate * self.decm, 2*self.ch1_baud, 1e3) ))

    def get_water_range(self):
        return self.water_range

    def set_water_range(self, water_range):
        self.water_range = water_range
        self._water_range_config_config = ConfigParser.ConfigParser()
        self._water_range_config_config.read(self.cfg_filename)
        if not self._water_range_config_config.has_section("settings"):
        	self._water_range_config_config.add_section("settings")
        self._water_range_config_config.set("settings", "water_range", str(self.water_range))
        self._water_range_config_config.write(open(self.cfg_filename, 'w'))
        self.qtgui_waterfall_sink_x_0.set_intensity_range(self.water_max - self.water_range, self.water_max)

    def get_water_max(self):
        return self.water_max

    def set_water_max(self, water_max):
        self.water_max = water_max
        self._water_max_config_config = ConfigParser.ConfigParser()
        self._water_max_config_config.read(self.cfg_filename)
        if not self._water_max_config_config.has_section("settings"):
        	self._water_max_config_config.add_section("settings")
        self._water_max_config_config.set("settings", "water_max", str(self.water_max))
        self._water_max_config_config.write(open(self.cfg_filename, 'w'))
        self.qtgui_waterfall_sink_x_0.set_intensity_range(self.water_max - self.water_range, self.water_max)

    def get_version(self):
        return self.version

    def set_version(self, version):
        self.version = version

    def get_usrp_tx_label(self):
        return self.usrp_tx_label

    def set_usrp_tx_label(self, usrp_tx_label):
        self.usrp_tx_label = usrp_tx_label
        Qt.QMetaObject.invokeMethod(self._usrp_tx_label_label, "setText", Qt.Q_ARG("QString", str(self.usrp_tx_label)))

    def get_usrp_rx_label(self):
        return self.usrp_rx_label

    def set_usrp_rx_label(self, usrp_rx_label):
        self.usrp_rx_label = usrp_rx_label
        Qt.QMetaObject.invokeMethod(self._usrp_rx_label_label, "setText", Qt.Q_ARG("QString", str(self.usrp_rx_label)))

    def get_usrp_addr(self):
        return self.usrp_addr

    def set_usrp_addr(self, usrp_addr):
        self.usrp_addr = usrp_addr

    def get_rx_data_tcp_ip(self):
        return self.rx_data_tcp_ip

    def set_rx_data_tcp_ip(self, rx_data_tcp_ip):
        self.rx_data_tcp_ip = rx_data_tcp_ip

    def get_period_config(self):
        return self.period_config

    def set_period_config(self, period_config):
        self.period_config = period_config

    def get_period(self):
        return self.period

    def set_period(self, period):
        self.period = period
        self._period_config_config = ConfigParser.ConfigParser()
        self._period_config_config.read(self.cfg_filename)
        if not self._period_config_config.has_section("settings"):
        	self._period_config_config.add_section("settings")
        self._period_config_config.set("settings", "period", str(self.period))
        self._period_config_config.write(open(self.cfg_filename, 'w'))
        self.approx_power_0_0.set_averages(int(self.samp_rate / (1000.0/self.period)))
        self.approx_power_0.set_averages(int(self.samp_rate / (1000.0/self.period)))

    def get_config_tcp_ip(self):
        return self.config_tcp_ip

    def set_config_tcp_ip(self, config_tcp_ip):
        self.config_tcp_ip = config_tcp_ip

    def get_ch2_tx_freq_label(self):
        return self.ch2_tx_freq_label

    def set_ch2_tx_freq_label(self, ch2_tx_freq_label):
        self.ch2_tx_freq_label = ch2_tx_freq_label
        Qt.QMetaObject.invokeMethod(self._ch2_tx_freq_label_label, "setText", Qt.Q_ARG("QString", str(self.ch2_tx_freq_label)))

    def get_ch2_tx_en_label(self):
        return self.ch2_tx_en_label

    def set_ch2_tx_en_label(self, ch2_tx_en_label):
        self.ch2_tx_en_label = ch2_tx_en_label
        Qt.QMetaObject.invokeMethod(self._ch2_tx_en_label_label, "setText", Qt.Q_ARG("QString", str(self.ch2_tx_en_label)))

    def get_ch2_threshold(self):
        return self.ch2_threshold

    def set_ch2_threshold(self, ch2_threshold):
        self.ch2_threshold = ch2_threshold
        self._ch2_threshold_config_config = ConfigParser.ConfigParser()
        self._ch2_threshold_config_config.read(self.cfg_filename)
        if not self._ch2_threshold_config_config.has_section("settings"):
        	self._ch2_threshold_config_config.add_section("settings")
        self._ch2_threshold_config_config.set("settings", "ch2_threshold", str(self.ch2_threshold))
        self._ch2_threshold_config_config.write(open(self.cfg_filename, 'w'))
        self.tyvak_transmit_buffer_pdu_0_0.set_threshold(self.ch2_threshold)

    def get_ch2_rx_freq_label(self):
        return self.ch2_rx_freq_label

    def set_ch2_rx_freq_label(self, ch2_rx_freq_label):
        self.ch2_rx_freq_label = ch2_rx_freq_label
        Qt.QMetaObject.invokeMethod(self._ch2_rx_freq_label_label, "setText", Qt.Q_ARG("QString", str(self.ch2_rx_freq_label)))

    def get_ch2_rx_en_label(self):
        return self.ch2_rx_en_label

    def set_ch2_rx_en_label(self, ch2_rx_en_label):
        self.ch2_rx_en_label = ch2_rx_en_label
        Qt.QMetaObject.invokeMethod(self._ch2_rx_en_label_label, "setText", Qt.Q_ARG("QString", str(self.ch2_rx_en_label)))

    def get_ch2_rx_data_tcp_port(self):
        return self.ch2_rx_data_tcp_port

    def set_ch2_rx_data_tcp_port(self, ch2_rx_data_tcp_port):
        self.ch2_rx_data_tcp_port = ch2_rx_data_tcp_port

    def get_ch2_pwr(self):
        return self.ch2_pwr

    def set_ch2_pwr(self, ch2_pwr):
        self.ch2_pwr = ch2_pwr
        self.tyvak_transmit_buffer_pdu_0_0.set_rx_power(self.ch2_pwr)

    def get_ch2_fft_range(self):
        return self.ch2_fft_range

    def set_ch2_fft_range(self, ch2_fft_range):
        self.ch2_fft_range = ch2_fft_range
        self._ch2_fft_range_config_config = ConfigParser.ConfigParser()
        self._ch2_fft_range_config_config.read(self.cfg_filename)
        if not self._ch2_fft_range_config_config.has_section("settings"):
        	self._ch2_fft_range_config_config.add_section("settings")
        self._ch2_fft_range_config_config.set("settings", "ch2_fft_range", str(self.ch2_fft_range))
        self._ch2_fft_range_config_config.write(open(self.cfg_filename, 'w'))
        self.qtgui_freq_sink_x_0.set_y_axis(self.ch2_fft_max - self.ch2_fft_range, self.ch2_fft_max)

    def get_ch2_fft_max(self):
        return self.ch2_fft_max

    def set_ch2_fft_max(self, ch2_fft_max):
        self.ch2_fft_max = ch2_fft_max
        self._ch2_fft_max_config_config = ConfigParser.ConfigParser()
        self._ch2_fft_max_config_config.read(self.cfg_filename)
        if not self._ch2_fft_max_config_config.has_section("settings"):
        	self._ch2_fft_max_config_config.add_section("settings")
        self._ch2_fft_max_config_config.set("settings", "ch2_fft_max", str(self.ch2_fft_max))
        self._ch2_fft_max_config_config.write(open(self.cfg_filename, 'w'))
        self.qtgui_freq_sink_x_0.set_y_axis(self.ch2_fft_max - self.ch2_fft_range, self.ch2_fft_max)

    def get_ch2_config_tcp_port(self):
        return self.ch2_config_tcp_port

    def set_ch2_config_tcp_port(self, ch2_config_tcp_port):
        self.ch2_config_tcp_port = ch2_config_tcp_port

    def get_ch2_bt_label_0(self):
        return self.ch2_bt_label_0

    def set_ch2_bt_label_0(self, ch2_bt_label_0):
        self.ch2_bt_label_0 = ch2_bt_label_0
        Qt.QMetaObject.invokeMethod(self._ch2_bt_label_0_label, "setText", Qt.Q_ARG("QString", str(self.ch2_bt_label_0)))

    def get_ch2_baud_label_0(self):
        return self.ch2_baud_label_0

    def set_ch2_baud_label_0(self, ch2_baud_label_0):
        self.ch2_baud_label_0 = ch2_baud_label_0
        Qt.QMetaObject.invokeMethod(self._ch2_baud_label_0_label, "setText", Qt.Q_ARG("QString", str(self.ch2_baud_label_0)))

    def get_ch1_tx_gain_label(self):
        return self.ch1_tx_gain_label

    def set_ch1_tx_gain_label(self, ch1_tx_gain_label):
        self.ch1_tx_gain_label = ch1_tx_gain_label
        Qt.QMetaObject.invokeMethod(self._ch1_tx_gain_label_label, "setText", Qt.Q_ARG("QString", str(self.ch1_tx_gain_label)))

    def get_ch1_tx_freq_label(self):
        return self.ch1_tx_freq_label

    def set_ch1_tx_freq_label(self, ch1_tx_freq_label):
        self.ch1_tx_freq_label = ch1_tx_freq_label
        Qt.QMetaObject.invokeMethod(self._ch1_tx_freq_label_label, "setText", Qt.Q_ARG("QString", str(self.ch1_tx_freq_label)))

    def get_ch1_tx_en_label(self):
        return self.ch1_tx_en_label

    def set_ch1_tx_en_label(self, ch1_tx_en_label):
        self.ch1_tx_en_label = ch1_tx_en_label
        Qt.QMetaObject.invokeMethod(self._ch1_tx_en_label_label, "setText", Qt.Q_ARG("QString", str(self.ch1_tx_en_label)))

    def get_ch1_threshold(self):
        return self.ch1_threshold

    def set_ch1_threshold(self, ch1_threshold):
        self.ch1_threshold = ch1_threshold
        self._ch1_threshold_config_config = ConfigParser.ConfigParser()
        self._ch1_threshold_config_config.read(self.cfg_filename)
        if not self._ch1_threshold_config_config.has_section("settings"):
        	self._ch1_threshold_config_config.add_section("settings")
        self._ch1_threshold_config_config.set("settings", "ch1_threshold", str(self.ch1_threshold))
        self._ch1_threshold_config_config.write(open(self.cfg_filename, 'w'))
        self.tyvak_transmit_buffer_pdu_0.set_threshold(self.ch1_threshold)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_AUTO, qtgui.TRIG_SLOPE_NEG, self.ch1_threshold, 0.25, 1, "")

    def get_ch1_rx_gain_label(self):
        return self.ch1_rx_gain_label

    def set_ch1_rx_gain_label(self, ch1_rx_gain_label):
        self.ch1_rx_gain_label = ch1_rx_gain_label
        Qt.QMetaObject.invokeMethod(self._ch1_rx_gain_label_label, "setText", Qt.Q_ARG("QString", str(self.ch1_rx_gain_label)))

    def get_ch1_rx_freq_label(self):
        return self.ch1_rx_freq_label

    def set_ch1_rx_freq_label(self, ch1_rx_freq_label):
        self.ch1_rx_freq_label = ch1_rx_freq_label
        Qt.QMetaObject.invokeMethod(self._ch1_rx_freq_label_label, "setText", Qt.Q_ARG("QString", str(self.ch1_rx_freq_label)))

    def get_ch1_rx_en_label(self):
        return self.ch1_rx_en_label

    def set_ch1_rx_en_label(self, ch1_rx_en_label):
        self.ch1_rx_en_label = ch1_rx_en_label
        Qt.QMetaObject.invokeMethod(self._ch1_rx_en_label_label, "setText", Qt.Q_ARG("QString", str(self.ch1_rx_en_label)))

    def get_ch1_rx_data_tcp_port(self):
        return self.ch1_rx_data_tcp_port

    def set_ch1_rx_data_tcp_port(self, ch1_rx_data_tcp_port):
        self.ch1_rx_data_tcp_port = ch1_rx_data_tcp_port

    def get_ch1_pwr(self):
        return self.ch1_pwr

    def set_ch1_pwr(self, ch1_pwr):
        self.ch1_pwr = ch1_pwr
        self.tyvak_transmit_buffer_pdu_0.set_rx_power(self.ch1_pwr)

    def get_ch1_fft_range(self):
        return self.ch1_fft_range

    def set_ch1_fft_range(self, ch1_fft_range):
        self.ch1_fft_range = ch1_fft_range
        self._ch1_fft_range_config_config = ConfigParser.ConfigParser()
        self._ch1_fft_range_config_config.read(self.cfg_filename)
        if not self._ch1_fft_range_config_config.has_section("settings"):
        	self._ch1_fft_range_config_config.add_section("settings")
        self._ch1_fft_range_config_config.set("settings", "ch1_fft_range", str(self.ch1_fft_range))
        self._ch1_fft_range_config_config.write(open(self.cfg_filename, 'w'))
        self.qtgui_freq_sink_x_0_0.set_y_axis(self.ch1_fft_max - self.ch1_fft_range, self.ch1_fft_max)

    def get_ch1_fft_max(self):
        return self.ch1_fft_max

    def set_ch1_fft_max(self, ch1_fft_max):
        self.ch1_fft_max = ch1_fft_max
        self._ch1_fft_max_config_config = ConfigParser.ConfigParser()
        self._ch1_fft_max_config_config.read(self.cfg_filename)
        if not self._ch1_fft_max_config_config.has_section("settings"):
        	self._ch1_fft_max_config_config.add_section("settings")
        self._ch1_fft_max_config_config.set("settings", "ch1_fft_max", str(self.ch1_fft_max))
        self._ch1_fft_max_config_config.write(open(self.cfg_filename, 'w'))
        self.qtgui_freq_sink_x_0_0.set_y_axis(self.ch1_fft_max - self.ch1_fft_range, self.ch1_fft_max)

    def get_ch1_config_tcp_port(self):
        return self.ch1_config_tcp_port

    def set_ch1_config_tcp_port(self, ch1_config_tcp_port):
        self.ch1_config_tcp_port = ch1_config_tcp_port

    def get_ch1_bt_label(self):
        return self.ch1_bt_label

    def set_ch1_bt_label(self, ch1_bt_label):
        self.ch1_bt_label = ch1_bt_label
        Qt.QMetaObject.invokeMethod(self._ch1_bt_label_label, "setText", Qt.Q_ARG("QString", str(self.ch1_bt_label)))

    def get_ch1_baud_label(self):
        return self.ch1_baud_label

    def set_ch1_baud_label(self, ch1_baud_label):
        self.ch1_baud_label = ch1_baud_label
        Qt.QMetaObject.invokeMethod(self._ch1_baud_label_label, "setText", Qt.Q_ARG("QString", str(self.ch1_baud_label)))


def main(top_block_cls=Tyvak_GS, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
