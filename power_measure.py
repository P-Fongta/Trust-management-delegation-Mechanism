#!/usr/bin/env python
from ina219 import INA219
from ina219 import DeviceRangeError
import time
import os
from datetime import datetime
import sys
SHUNT_OHMS = 0.1


def read(arg):
    args = sys.argv[1:]
    ina = INA219(SHUNT_OHMS)
    ina.configure()
    with open("/home/pi/aiocoap/e-health/power_measure/power%s-%s.txt"%(args[0],args[1]), 'a') as file1:

        while True:
            #os.system('clear')
            VOLT=ina.voltage()
            print("Voltage: %.3f V" % VOLT, end=' ')
            try:
                CUR=ina.current()
                print("Current: %.3f mA" % CUR, end=' ')
                POW=ina.power()
                print("Power: %.3f mW" % POW)
                #print("Shunt voltage: %.3f mV" % ina.shunt_voltage())
            except DeviceRangeError as e:
                # Current out of device range with specified shunt resistor
                print(e)
            L=[str(f'{VOLT:.3f}')+' '+str(f'{CUR:.3f}')+' '+str(f'{POW:.3f}')+' '+datetime.now().strftime("%H:%M:%S")]
            file1.writelines(L)
            file1.write("\n")
            file1.flush()
            time.sleep(1)
        

if __name__ == "__main__":
    read(sys.argv[1:])