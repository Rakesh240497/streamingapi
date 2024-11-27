import requests
import json
import time

def subscribe_and_process_data():
    url = 'http://127.0.0.1:5000/stream-items'  # Flask API endpoint

    with requests.get(url, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    # Parse the JSON data from the SSE stream
                    data = json.loads(line.decode('utf-8').split('data: ')[1].strip())
                    print(f"Received data: {data}")
                    time.sleep(1) 
while(True):
    subscribe_and_process_data()
    time.sleep(1)
