import requests
import json
import time
from google.cloud import pubsub_v1
# from google.cloud import auth2
from google.cloud import storage
from google.auth.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account

projectid = 'startupproj-440220'
topicid = 'systemdata'

credentials_path = '/Users/rakeshnanankal/downloads/startupproj-440220-b1b200ed05d2.json'

# Initialize credentials and Pub/Sub client
credentials = None
try:
    # Load credentials from the service account file
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    print("Succesfully Authorized")
except Exception as e:
    print(f"Error Occurred While Validating GCloud: {e}")

publisher = pubsub_v1.PublisherClient(credentials=credentials)

topic_path = publisher.topic_path(project=projectid, topic=topicid)

def assing_values(data):
    message = {
    "cpu_usage_percent": data['cpu']['usage_percent'],
    "cpu_frequency_mhz": data['cpu']['frequency_mhz'],
    
    "memory_total": data['memory']['total'],
    "memory_available": data['memory']['available'],
    "memory_percent": data['memory']['percent'],
    "memory_used": data['memory']['used'],
    "memory_free": data['memory']['free'],
    
    "swap_total": data['memory']['swap']['total'],
    "swap_used": data['memory']['swap']['used'],
    "swap_free": data['memory']['swap']['free'],
    "swap_percent": data['memory']['swap']['percent'],
    
    "disk_total": data['disk']['total'],
    "disk_used": data['disk']['used'],
    "disk_free": data['disk']['free'],
    "disk_percent": data['disk']['percent'],
    
    "disk_io_read_bytes": data['disk']['io']['read_bytes'],
    "disk_io_write_bytes": data['disk']['io']['write_bytes'],
    "disk_io_read_time": data['disk']['io']['read_time'],
    "disk_io_write_time": data['disk']['io']['write_time'],
    
    "network_bytes_sent": data['network']['bytes_sent'],
    "network_bytes_received": data['network']['bytes_received'],
    "network_packets_sent": data['network']['packets_sent'],
    "network_packets_received": data['network']['packets_received'],
    
    "battery_percent": data['battery']['percent'],
    "battery_secs_left": data['battery']['secs_left'],
    "battery_power_plugged": data['battery']['power_plugged']
    }

    return message


def publish_to_pubsub(message):
    data_str = json.dumps(message)
    data_bytes = data_str.encode('utf-8')
    publisher.publish(topic_path, data=data_bytes)
    print(f"Published message to {topic_path}")


def subscribe_and_process_data():
    url = 'http://127.0.0.1:5000/cpudata'  # Flask API endpoint
    try:
        with requests.get(url, stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    # Ensure the line is non-empty and starts with `data: `
                    if line:
                        try:
                            # Decode the line and process JSON
                            decoded_line = line.decode('utf-8')
                            if decoded_line.startswith('data: '):
                                json_data = json.loads(decoded_line.split('data: ', 1)[1].strip())
                                message = assing_values(json_data)
                                publish_to_pubsub(message)
                                print(f"Processed JSON Data: {assing_values(json_data)}")
                            else:
                                print(f"Ignored Non-Data Line: {decoded_line}")
                        except json.JSONDecodeError as e:
                            print(f"JSON Decode Error: {e} for line: {decoded_line}")
            else:
                print(f"Failed to connect. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

subscribe_and_process_data()

