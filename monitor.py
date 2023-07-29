# Imports
import requests
import time

# Variables
status_url = 'http://hdhomerun.local/status.json'
mil = 1000000
expected_tuner_data_len = 9
print_to_console = False

# Request to HDHR
req_start_time = time.perf_counter_ns()
response = requests.get(status_url)
req_end_time = time.perf_counter_ns()
request_time = round((req_end_time - req_start_time) / mil)

# Parse JSON response
if response.status_code == 200:
    json_data = response.json()

    # Parse Tuner 0
    if len(json_data[0]) == expected_tuner_data_len:
        t0_channel = json_data[0]['VctNumber']
        t0_name = json_data[0]['VctName']
        t0_freq = round((json_data[0]['Frequency'] / mil))
        t0_strength = json_data[0]['SignalStrengthPercent']
        t0_quality = json_data[0]['SignalQualityPercent']
        t0_symbol = json_data[0]['SymbolQualityPercent']
        t0_bitrate = round((json_data[0]['NetworkRate'] / mil), 2)
        if print_to_console:
            print(f"Tuner 0:\n"
                  f"\tCH: {t0_channel}\n"
                  f"\tCS: {t0_name}\n"
                  f"\tFQ: {t0_freq} Mhz\n"
                  f"\tST: {t0_strength}%\n"
                  f"\tQU: {t0_quality}%\n"
                  f"\tSY: {t0_symbol}%\n"
                  f"\tBR: {t0_bitrate} Mbps\n")
    else:
        print("Tuner 0:\n"
              "\tInactive\n")

    # Parse Tuner 1
    if len(json_data[1]) == expected_tuner_data_len:
        t1_channel = json_data[1]['VctNumber']
        t1_name = json_data[1]['VctName']
        t1_freq = round((json_data[1]['Frequency'] / mil))
        t1_strength = json_data[1]['SignalStrengthPercent']
        t1_quality = json_data[1]['SignalQualityPercent']
        t1_symbol = json_data[1]['SymbolQualityPercent']
        t1_bitrate = round((json_data[1]['NetworkRate'] / mil), 2)
        if print_to_console:
            print(f"Tuner 1:\n"
                  f"\tCH: {t1_channel}\n"
                  f"\tCS: {t1_name}\n"
                  f"\tFQ: {t1_freq} Mhz\n"
                  f"\tST: {t1_strength}%\n"
                  f"\tQU: {t1_quality}%\n"
                  f"\tSY: {t1_symbol}%\n"
                  f"\tBR: {t1_bitrate} Mbps\n")
    else:
        print("Tuner 1:\n"
              "\tInactive\n")

else:
    print(f"Error: Received status code {response.status_code}")

print(f"Response took {request_time} ms")
