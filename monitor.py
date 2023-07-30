# Imports
import requests
import time
from tabulate import tabulate

# Variables
status_url = 'http://hdhomerun.local/status.json'
mil = 1000000
tuners = [0, 1]
stations = [{"freq": 539, "rf": 25, "location": "BWI"},
            {"freq": 587, "rf": 33, "location": "DCA"}]
status = [['Tuner', 'Channel', 'RF', 'Loc', 'Name', 'ST', 'QU', 'SY']]
tabulate_align = ("center","center","center","center","center","right","right","right",)
# 5 when using config, 9 when tuned
expected_tuner_data_len = [5, 9]

# Request to HDHR
req_start_time = time.perf_counter_ns()
response = requests.get(status_url)
req_end_time = time.perf_counter_ns()
request_time = round((req_end_time - req_start_time) / mil)

# Parse JSON response
if response.status_code == 200:
    json_data = response.json()

    active_tuners = 0
    for tuner in tuners:
        if len(json_data[tuner]) in expected_tuner_data_len:
            try:
                channel = json_data[tuner]['VctNumber']
            except KeyError:
                channel = "-"
            try:
                name = json_data[tuner]['VctName']
            except KeyError:
                name = "--"
            freq = round((json_data[tuner]['Frequency'] / mil))
            rf = "--"
            location = "---"
            for station in stations:
                if station['freq'] == freq:
                    rf = station['rf']
                    location = station['location']
                    break
            strength = json_data[tuner]['SignalStrengthPercent']
            quality = json_data[tuner]['SignalQualityPercent']
            symbol = json_data[tuner]['SymbolQualityPercent']
            # try:
            #     bitrate = round((json_data[tuner]['NetworkRate'] / mil), 2)
            # except KeyError:
            #     bitrate = "n/a"
            status.append([tuner,
                           channel,
                           rf,
                           location,
                           name,
                           str(strength) + '%',
                           str(quality) + '%',
                           str(symbol) + '%'])
            active_tuners += 1

    if active_tuners:
        print(tabulate(status, headers="firstrow", tablefmt="simple_outline",
                       colalign=tabulate_align))
    else:
        print("No tuners active")

else:
    print(f"Error: Received status code {response.status_code}")

print(f"Response took {request_time} ms")
