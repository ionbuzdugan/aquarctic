import nidaqmx
import time
import csv

import pandas as pd

from nidaqmx.constants import ThermocoupleType, TemperatureUnits
from datetime import datetime as dt

LOG_PERIOD = 0
FILENAME = 'TEST'
TC_NAMES = ['TC1','TC2','TC3']

filename = 'LOGS/'+dt.now().strftime('%Y-%m-%d-%H-%M-%S')+'_'+FILENAME+'.csv'
with open(filename,'w',newline='') as file:
    wr = csv.writer(file, quoting=csv.QUOTE_NONE)
    wr.writerow(['epoch']+TC_NAMES)

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_thrmcpl_chan(
        "cDAQ1Mod1/ai0", units=TemperatureUnits.DEG_C, thermocouple_type=ThermocoupleType.K
    )
    task.ai_channels.add_ai_thrmcpl_chan(
        "cDAQ1Mod1/ai1", units=TemperatureUnits.DEG_C, thermocouple_type=ThermocoupleType.K
    )
    task.ai_channels.add_ai_thrmcpl_chan(
        "cDAQ1Mod1/ai2", units=TemperatureUnits.DEG_C, thermocouple_type=ThermocoupleType.K
    )
    while True:
        data = task.read()
        print(f"Acquired data: {data}",flush=True)
        with open(filename,'a',newline='') as file:
            wr = csv.writer(file, quoting=csv.QUOTE_NONE)
            wr.writerow([time.time()]+data)
        time.sleep(LOG_PERIOD)