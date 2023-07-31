# Imports
import requests
import time
from tabulate import tabulate

script_start_time = time.perf_counter_ns()

# Variables
status_url = 'http://hdhomerun.local/status.json'
mil = 1000000  # 1 million to simplify later calculations
tuners = [0, 1]
stations = [{"freq": 539, "rf": 25, "location": "BWI"},
            {"freq": 587, "rf": 33, "location": "DCA"}]
status = [['Tuner', 'Channel', 'RF', 'Loc', 'Name', 'ST', 'QU', 'SY']]
tabulate_align = ("center", "center", "center", "center", "center", "right", "right", "right",)
expected_tuner_data_len = [5, 9]  # 5 when using config tool, 9 when tuned

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

            # Try VctNumber and VctName because config tool does not actually attach to a channel
            try:
                channel = json_data[tuner]['VctNumber']
            except KeyError:
                channel = "-"
            try:
                name = json_data[tuner]['VctName']
            except KeyError:
                name = "--"

            # Grab reported frequency and divide by 1 million to simplify
            freq = round((json_data[tuner]['Frequency'] / mil))

            # Try to map the reported frequency to an RF channel and location
            rf = "--"
            location = "---"
            for station in stations:
                if station['freq'] == freq:
                    rf = station['rf']
                    location = station['location']
                    break

            # Grab signal strength, signal quality, and symbol quality
            strength = json_data[tuner]['SignalStrengthPercent']
            quality = json_data[tuner]['SignalQualityPercent']
            symbol = json_data[tuner]['SymbolQualityPercent']

            # Grab reported bitrate of stream
            # try:
            #     bitrate = round((json_data[tuner]['NetworkRate'] / mil), 2)
            # except KeyError:
            #     bitrate = "n/a"

            # Add to the "status" array
            status.append([tuner,
                           channel,
                           rf,
                           location,
                           name,
                           str(strength) + '%',
                           str(quality) + '%',
                           str(symbol) + '%'])

            # Increment the counter if any tuners are active
            active_tuners += 1

    # If a tuner is active, print out status data
    if active_tuners:
        print(tabulate(status, headers="firstrow", tablefmt="simple_outline",
                       colalign=tabulate_align))
    else:
        print("No tuners active")

else:
    print(f"Error: Received status code {response.status_code}")

print(f"Response took {request_time} ms")

script_end_time = time.perf_counter_ns()
script_time = round((script_end_time - script_start_time) / mil)
print(f"Script took {script_time} ms")
