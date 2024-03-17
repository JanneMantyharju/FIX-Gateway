#!/usr/bin/env python

#  Copyright (c) 2019 Phil Birkelbach
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307,
#  USA.import plugin

#  This is a simple data simulation plugin.  It's mainly for demo purposese
#  It really has no function other than simple testing of displays

# TODO Make the keylist configurable
# TODO add some functions to change the values (noise, cyclic, reduction, etc)

import threading
import time
from collections import OrderedDict
import fixgw.plugin as plugin

class MainThread(threading.Thread):
    def __init__(self, parent):
        super(MainThread, self).__init__()
        self.getout = False   # indicator for when to stop
        self.parent = parent  # parent plugin object
        self.log = parent.log  # simplifies logging
        self.keylist = {"ROLL":0.0, "PITCH":0.0, "IAS":113.0, "ALT":1153.0, "VS": 0,
                        "TACH1":2450.0, "MAP1":24.2, "FUELP1":28.5, "OILP1":56.4,
                        "OILT1":95.0, "FUELQ1":11.2, "FUELQ2":19.8, "FUELQ3":10.8,"OAT": 32.0,
                        "CHT11":201.0,"CHT12":202.0,"CHT13":199.0,"CHT14":200.0,
                        "EGT11":510.0,"EGT12":540.0,"EGT13":544.0,"EGT14":522.0,
                        "FUELF1":8.7,"VOLT":13.7,"CURRNT":45.6,
                        "TAS":113,"ALAT":0.0,"HEAD":281.8,"LONG":-82.8550,"LAT":40.000200,
                        "CDI":0.0,"GSI":0.0,"COURSE":281.8,
                        "COMTXPWR1": 0, "COMVSWR1": 0, "COMACTTX1": False, "COMSTDRXLEVEL1": 0,
                        "COMACTRXLEVEL1": 0, "COMSQUELCH1": 4.5, "COMACTRX1": False, "COMSTDRX1": False,
                        "COMAUDVOL1": 10, "COMRXVOL1":9, "COMINTVOL1":10,
                        "COMACTFREQ1": 121.500, "COMSTDFREQ1": 121.500
                        }
        self.script = [

            {"APMSG": "Roll/Pitch 0",     "ROLL": 0,   "PITCH": 0 },
            {"APMSG": "Roll/Pitch 10",    "ROLL": 10,  "PITCH": 10 },
            {"APMSG": "Roll/Pitch 20",    "ROLL": 20,  "PITCH": 20 },
            {"APMSG": "Roll/Pitch 10",    "ROLL": 10,  "PITCH": 10 },
            {"APMSG": "Roll/Pitch 0",     "ROLL": 0,   "PITCH": 0 },
            {"APMSG": "Roll/Pitch 10",    "ROLL": -10, "PITCH": -10 },
            {"APMSG": "Roll/Pitch 20",    "ROLL": -20, "PITCH": -20 },
            {"APMSG": "Roll/Pitch 10",    "ROLL": -10, "PITCH": -10 },
            {"APMSG": "Roll/Pitch 0",     "ROLL": 0,   "PITCH": 0 },
            {"APMSG": "PAPI 2 Red",       "ALT": 1153 },
            {"APMSG": "PAPI 1 Red",       "ALT": 1200 },
            {"APMSG": "PAPI 0 Red",       "ALT": 1250 },
            {"APMSG": "PAPI 1 Red",       "ALT": 1200 },
            {"APMSG": "PAPI 2 Red",       "ALT": 1153 },
            {"APMSG": "PAPI 3 Red",       "ALT": 1100 },
            {"APMSG": "PAPI 4 Red",       "ALT": 1050 },
            {"APMSG": "PAPI 3 Red",       "ALT": 1100 },
            {"APMSG": "PAPI 2 Red",       "ALT": 1153 },
            {"APMSG": "HEAD 281",         "HEAD": 281.8 },
            {"APMSG": "HEAD 254",         "HEAD": 254 },
            {"APMSG": "HEAD 234",         "HEAD": 234 },
            {"APMSG": "HEAD 214",         "HEAD": 214 },
            {"APMSG": "HEAD 194",         "HEAD": 194 },
            {"APMSG": "HEAD 174",         "HEAD": 174 },
            {"APMSG": "HEAD 154",         "HEAD": 154 },
            {"APMSG": "HEAD 134",         "HEAD": 134 },
            {"APMSG": "HEAD 114",         "HEAD": 114 },
            {"APMSG": "HEAD 94",          "HEAD": 94 },
            {"APMSG": "HEAD 74",          "HEAD": 74 },
            {"APMSG": "HEAD 54",          "HEAD": 54 },
            {"APMSG": "HEAD 34",          "HEAD": 34 },
            {"APMSG": "HEAD 14",          "HEAD": 14 },
            {"APMSG": "HEAD 0",           "HEAD": 0 },
            {"APMSG": "HEAD 14",          "HEAD": 14 },
            {"APMSG": "HEAD 34",          "HEAD": 34 },
            {"APMSG": "HEAD 54",          "HEAD": 54 },
            {"APMSG": "HEAD 74",          "HEAD": 74 },
            {"APMSG": "HEAD 94",          "HEAD": 94 },
            {"APMSG": "HEAD 114",         "HEAD": 114 },
            {"APMSG": "HEAD 134",         "HEAD": 134 },
            {"APMSG": "HEAD 154",         "HEAD": 154 },
            {"APMSG": "HEAD 174",         "HEAD": 174 },
            {"APMSG": "HEAD 194",         "HEAD": 194 },
            {"APMSG": "HEAD 214",         "HEAD": 214 },
            {"APMSG": "HEAD 234",         "HEAD": 234 },
            {"APMSG": "HEAD 254",         "HEAD": 254 },
            {"APMSG": "HEAD 281",         "HEAD": 281.8 },
            {"APMSG": "Landing",           "HEAD":281.8, "LONG": -82.8550, "LAT":40.000200, "ALT": 1153, "VS": -300},
            {"APMSG": "Landing",           "HEAD":281.8, "LONG": -82.8650, "LAT":40.000750, "ALT": 1020, "VS": -300},
            {"APMSG": "Landing",           "HEAD":281.8, "LONG": -82.8750, "LAT":40.001350, "ALT": 880, "VS": -300},
            {"APMSG": "Landing",           "HEAD":281.8, "LONG": -82.8780, "LAT":40.001530, "ALT": 860, "VS": -300},
            {"APMSG": "Landing",           "HEAD":281.8, "LONG": -82.8789, "LAT":40.00160, "ALT": 830, "VS": -300},
            {"APMSG": "Reverse Landing",   "HEAD":281.8, "LONG": -82.8780, "LAT":40.001530, "ALT": 860, "VS": 300},
            {"APMSG": "Reverse Landing",   "HEAD":281.8, "LONG": -82.8750, "LAT":40.001350, "ALT": 880, "VS": 300},
            {"APMSG": "Reverse Landing",   "HEAD":281.8, "LONG": -82.8650, "LAT":40.000750, "ALT": 1020, "VS": 300},
            {"APMSG": "Reverse Landing",   "HEAD":281.8, "LONG": -82.8550, "LAT":40.000200, "ALT": 1153, "VS": 300},


            {"APMSG": "Encoder left 1",     "ENC3": "-1"},
            {"APMSG": "Encoder right 1",     "ENC3": "1"},
            {"APMSG": "Encoder right 2",     "ENC3": "1"},
            {"APMSG": "Encoder right 3",     "ENC3": "1", "BTN3": "False"},
            {"APMSG": "Encoder Button press",     "BTN3": "True"},
            {"APMSG": "Encoder left 1",     "ENC3": "-1"},
            {"APMSG": "Encoder left 2",     "ENC3": "-1", "BTN3": "False"},
            {"APMSG": "Encoder Button press 1",     "BTN3": "True"},
            {"APMSG": "Encoder Button press 1", "BTN3": "False"},
            {"APMSG": "Encoder Button press 2",     "BTN3": "True"},
            {"APMSG": "Encoder right 1",     "ENC3": "1"},
            {"APMSG": "Encoder right 2",     "ENC3": "1", "BTN3": "False"},
            {"APMSG": "Encoder Button press",     "BTN3": "True"},
            {"APMSG": "Wait for encoder timeout 1"},
            {"APMSG": "Wait for encoder timeout 2"},
            {"APMSG": "Wait for encoder timeout 3"},
            {"APMSG": "Wait for encoder timeout 4"},
            {"APMSG": "Wait for encoder timeout 5"},
            {"APMSG": "Wait for encoder timeout 6"},
            {"APMSG": "Wait for encoder timeout 7"},
            {"APMSG": "Wait for encoder timeout 8"},
            {"APMSG": "Wait for encoder timeout 9"},

            {"APMSG": "Encoder right 1",     "ENC3": "1"},
            {"APMSG": "Encoder right 2",     "ENC3": "1", "BTN3": "False"},
            {"APMSG": "Encoder right 3",     "ENC3": "1"},
            {"APMSG": "Encoder right 4",     "ENC3": "1"},
            {"APMSG": "Encoder right 5",     "ENC3": "1"},
            {"APMSG": "Encoder Button press 1",     "BTN3": "True"},
            {"APMSG": "Encoder left 1",     "ENC3": "-1"},
            {"APMSG": "Encoder left 2",     "ENC3": "-1"},
            {"APMSG": "Encoder left 3",     "ENC3": "-1"},
            {"APMSG": "Encoder left 4",     "ENC3": "-1"},




            {"APMSG": "IAS/TAS 113",       "IAS": 113, "TAS": 113, "VS": 0 },
            {"APMSG": "IAS/TAS 123",       "IAS": 123, "TAS": 123 },
            {"APMSG": "IAS/TAS 133",       "IAS": 133, "TAS": 133 },
            {"APMSG": "IAS/TAS 143",       "IAS": 143, "TAS": 143 },
            {"APMSG": "IAS/TAS 133",       "IAS": 133, "TAS": 133 },
            {"APMSG": "IAS/TAS 123",       "IAS": 123, "TAS": 123 },
            {"APMSG": "IAS/TAS 113",       "IAS": 113, "TAS": 113 },
            {"APMSG": "COURSE 281, VS 100, ALAT -.05",         "COURSE": 281.8, "VS": 100,  "ALAT": -.05 },
            {"APMSG": "COURSE 254, VS 500, ALAT -.1",         "COURSE": 254,   "VS": 500,  "ALAT": -.1 },
            {"APMSG": "COURSE 234, VS 900, ALAT -.2",         "COURSE": 234,   "VS": 900,  "ALAT": -.2 },
            {"APMSG": "COURSE 214, VS 1200,ALAT -.3",         "COURSE": 214,   "VS": 1200, "ALAT": -.3 },
            {"APMSG": "COURSE 194, VS 1500,ALAT 0",          "COURSE": 194,   "VS": 1500, "ALAT": 0 },
            {"APMSG": "COURSE 214, VS 1200,ALAT .1",           "COURSE": 214,   "VS": 1200, "ALAT": .1 },
            {"APMSG": "COURSE 234, VS 900,ALAT .2",           "COURSE": 234,   "VS": 900,  "ALAT": .2 },
            {"APMSG": "COURSE 254, VS 500,ALAT .3",           "COURSE": 254,   "VS": 500,  "ALAT": .3 },
            {"APMSG": "COURSE 281, VS 0, ALAT 0",           "COURSE": 281.8, "VS": 00,  "ALAT": 0 },
            {"APMSG": "CHT 100, EGT 500, FUELQ 21,21,42",    "CHT11":100,"CHT11":100,"CHT12":100,"CHT13":100,"CHT14":100,"EGT11":500,"EGT12":500,"EGT13":500,"EGT14":500,"FUELQ1":21,"FUELQ2": 21, "FUELQ3": 42 },
            {"APMSG": "CHT 150, EGT 550, FUELQ 18,17,38",    "CHT11":150,"CHT11":150,"CHT12":150,"CHT13":150,"CHT14":150,"EGT11":550,"EGT12":550,"EGT13":550,"EGT14":550,"FUELQ1":18,"FUELQ2": 17, "FUELQ3": 38 },
            {"APMSG": "CHT 200, EGT 600, FUELQ 15,15,30",    "CHT11":200,"CHT11":200,"CHT12":200,"CHT13":200,"CHT14":200,"EGT11":600,"EGT12":600,"EGT13":600,"EGT14":600,"FUELQ1":15,"FUELQ2": 15, "FUELQ3": 30 },
            {"APMSG": "CHT 250, EGT 650, FUELQ 10,11,20",    "CHT11":250,"CHT11":250,"CHT12":250,"CHT13":250,"CHT14":200,"EGT11":650,"EGT12":650,"EGT13":650,"EGT14":650,"FUELQ1":10,"FUELQ2": 11, "FUELQ3": 20 },
            {"APMSG": "CHT 300, EGT 680, FUELQ 5,6,10",      "CHT11":300,"CHT11":300,"CHT12":300,"CHT13":300,"CHT14":200,"EGT11":680,"EGT12":680,"EGT13":680,"EGT14":680,"FUELQ1":5,"FUELQ2": 6, "FUELQ3": 10 },
            {"APMSG": "CHT 320, EGT 750, FUELQ 0,0,0,0",     "CHT11":320,"CHT11":320,"CHT12":320,"CHT13":320,"CHT14":200,"EGT11":750,"EGT12":750,"EGT13":750,"EGT14":750,"FUELQ1":0,"FUELQ2": 0, "FUELQ3": 0 },
            {"APMSG": "CHT 320, EGT 750, FUELQ 0,0,0,0",     "CHT11":320,"CHT11":320,"CHT12":320,"CHT13":320,"CHT14":200,"EGT11":750,"EGT12":750,"EGT13":750,"EGT14":750,"FUELQ1":0,"FUELQ2": 0, "FUELQ3": 0 },
            {"APMSG": "CHT 300, EGT 680, FUELQ 5,6,10",      "CHT11":300,"CHT11":300,"CHT12":300,"CHT13":300,"CHT14":200,"EGT11":680,"EGT12":680,"EGT13":680,"EGT14":680,"FUELQ1":5,"FUELQ2": 6, "FUELQ3": 10 },
            {"APMSG": "CHT 250, EGT 650, FUELQ 10,11,20",    "CHT11":250,"CHT11":250,"CHT12":250,"CHT13":250,"CHT14":200,"EGT11":650,"EGT12":650,"EGT13":650,"EGT14":650,"FUELQ1":10,"FUELQ2": 11, "FUELQ3": 20 },
            {"APMSG": "CHT 200, EGT 600, FUELQ 15,15,30",    "CHT11":200,"CHT11":200,"CHT12":200,"CHT13":200,"CHT14":200,"EGT11":600,"EGT12":600,"EGT13":600,"EGT14":600,"FUELQ1":15,"FUELQ2": 15, "FUELQ3": 30 },
            {"APMSG": "CHT 150, EGT 550, FUELQ 18,17,38",    "CHT11":150,"CHT11":150,"CHT12":150,"CHT13":150,"CHT14":150,"EGT11":550,"EGT12":550,"EGT13":550,"EGT14":550,"FUELQ1":18,"FUELQ2": 17, "FUELQ3": 38 },
            {"APMSG": "CHT 100, EGT 500, FUELQ 21,21,42",    "CHT11":100,"CHT11":95,"CHT12":90,"CHT13":120,"CHT14":101,"EGT11":490,"EGT12":510,"EGT13":501,"EGT14":500,"FUELQ1":5,"FUELQ2": 11, "FUELQ3": 42 },
            {"APMSG": "TACH 3200, OILP: 0,  OILT 0,  MAP, 0",   "TACH1":3200,"OILP1":0,  "OILT1":0,  "MAP1":0 },
            {"APMSG": "TACH 2800, OILP: 20, OILT 24, MAP, 5",   "TACH1":2800,"OILP1":20, "OILT1":24, "MAP1":5 },
            {"APMSG": "TACH 2000, OILP: 40, OILT 44, MAP, 15",  "TACH1":2000,"OILP1":40, "OILT1":44, "MAP1":15 },
            {"APMSG": "TACH 1500, OILP: 60, OILT 64, MAP, 20",  "TACH1":1500,"OILP1":60, "OILT1":64, "MAP1":20 },
            {"APMSG": "TACH 1000, OILP: 80, OILT 84, MAP, 25",  "TACH1":1000,"OILP1":80, "OILT1":84, "MAP1":25 },
            {"APMSG": "TACH 500,  OILP: 90, OILT 100,MAP, 28",  "TACH1":500,"OILP1": 90, "OILT1":100,"MAP1":28 },
            {"APMSG": "TACH 0, OILP: 100, OILT 122, MAP,  30",  "TACH1":3200,"OILP1":100,"OILT1":122,"MAP1":30 },
            {"APMSG": "TACH 0, OILP: 100, OILT 122, MAP,  30",  "TACH1":3200,"OILP1":100,"OILT1":122,"MAP1":30 },
            {"APMSG": "TACH 500,  OILP: 90, OILT 100,MAP, 28",  "TACH1":500,"OILP1": 90, "OILT1":100,"MAP1":28 },
            {"APMSG": "TACH 1000, OILP: 80, OILT 84, MAP, 25",  "TACH1":1000,"OILP1":80, "OILT1":84, "MAP1":25 },
            {"APMSG": "TACH 1500, OILP: 60, OILT 64, MAP, 20",  "TACH1":1500,"OILP1":60, "OILT1":64, "MAP1":20 },
            {"APMSG": "TACH 2000, OILP: 40, OILT 44, MAP, 15",  "TACH1":2000,"OILP1":40, "OILT1":44, "MAP1":15 },
            {"APMSG": "TACH 2800, OILP: 20, OILT 24, MAP, 5",   "TACH1":2800,"OILP1":20, "OILT1":24, "MAP1":5 },
            {"APMSG": "TACH 3200, OILP: 0,  OILT 0,  MAP, 0",   "TACH1":3200,"OILP1":0,  "OILT1":0,  "MAP1":0 },
            {"APMSG": "TACH 2450, OILP: 60,  OILT 80,  MAP, 10",   "TACH1":2450,"OILP1":60,  "OILT1":80,  "MAP1":10 },
            {"APMSG": "RADIO vol",        "COMRXVOL1": 0, "COMINTVOL1": 0, "COMAUDVOL1": 0 },
            {"APMSG": "RADIO vol",        "COMRXVOL1": 10, "COMINTVOL1": 9, "COMAUDVOL1": 10 },
            {"APMSG": "RADIO tx" ,       "COMTXPWR1": 10, "COMVSWR1": 1.5, "COMACTTX1": True },
            {"APMSG": "RADIO tx" ,       "COMTXPWR1": 10, "COMVSWR1": 1.5, "COMACTTX1": True },
            {"APMSG": "RADIO idle",        "COMTXPWR1": 0, "COMVSWR1": 0, "COMACTTX1": False },
            {"APMSG": "RADIO rx"  ,      "COMACTRXLEVEL1": 10, "COMSQUELCH1": 4.5, "COMACTRX1": True },
            {"APMSG": "RADIO rx"  ,      "COMACTRXLEVEL1": 10, "COMSQUELCH1": 4.5, "COMACTRX1": True },
            {"APMSG": "RADIO rx"  ,      "COMACTRXLEVEL1": 0,  "COMSQUELCH1": 4.5, "COMACTRX1": False },
            {"APMSG": "RADIO standby rx"  ,      "COMSTDRXLEVEL1": 10, "COMSQUELCH1": 4.5, "COMSTDRX1": True },
            {"APMSG": "RADIO standby rx"  ,      "COMSTDRXLEVEL1": 10, "COMSQUELCH1": 4.5, "COMSTDRX1": True },
            {"APMSG": "RADIO standby rx"  ,      "COMSTDRXLEVEL1": 0, "COMSQUELCH1": 4.5, "COMSTDRX1": False },
            {"APMSG": "NO DATA"},



        ]
        # Initialize the points
        for each in self.keylist:
            self.parent.db_write(each, self.keylist[each])

    def run(self):
        count = 0
        script_count = -1
        script_when = -1
        while not self.getout:
            count += 1
            script_when += 1
            time.sleep(0.1)
            # We just read the point and write it back in to reset the TOL timer
            for each in self.keylist:
                x = self.parent.db_read(each)
                if each in ['LAT','LONG']:
                    y = x[0]
                    if (count % 2) == 0:
                        y += 0.0000001
                    else:
                        y -= 0.0000001
                    self.parent.db_write(each, y)
                else:
                    self.parent.db_write(each, x)
            #continue
            #print(f"script_when:{script_when}, script_count:{script_count}")
            if "NO DATA" == self.script[script_count]['APMSG']:
                self.parent.db_write("APMSG", "NO DATA")
                time.sleep(0.6)
            if script_when == 0:
                script_count += 1
                for k,v in self.script[script_count].items():
                    self.parent.db_write(k,v)
                    #print(f"{k}={v}")
                if script_count +1 == len(self.script):
                    script_count = -1
            else:
                if script_count  < len(self.script):
                    for k,v in self.script[script_count].items():
                        if not isinstance(v, str):
                            if self.script[script_count + 1].get(k,None) != None:
                                val = ( ( ( self.script[script_count + 1][k] - v ) / 20 ) * script_when ) + v
                                #print(f"{script_when}: next: {self.script[script_count + 1][k]}, cur:{v}, val:{val}")
                                self.parent.db_write(k,val)
                if script_when == 19:
                    script_when = -1
        self.running = False

    def stop(self):
        self.getout = True


class Plugin(plugin.PluginBase):
    def __init__(self, name, config):
        super(Plugin, self).__init__(name, config)
        self.thread = MainThread(self)
        self.status = OrderedDict()

    def run(self):

        self.thread.start()

    def stop(self):
        self.thread.stop()
        if self.thread.is_alive():
            self.thread.join(1.0)
        if self.thread.is_alive():
            raise plugin.PluginFail

    def get_status(self):
        return self.status
