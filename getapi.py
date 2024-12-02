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
topicid = 'streamingapi'

credentials_path = '/Users/rakeshnanankal/airflow/newworkspace/tempararyfiles/startupproj-440220-3ab43177dd3e.json'

# Initialize credentials and Pub/Sub client
credentials = None
try:
    # Load credentials from the service account file
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
except Exception as e:
    print(f"Error Occurred While Validating GCloud: {e}")

publisher = pubsub_v1.PublisherClient(credentials=credentials)

topic_path = publisher.topic_path(project=projectid, topic=topicid)
print("hello world")
def publish_to_pubsub(data):
    data_str = json.dumps(data)
    data_bytes = data_str.encode('utf-8')
    publisher.publish(topic_path, data=data_bytes)
    print(f"Published message to {topic_path}")



print("Hello Everyone")
def subscribe_and_process_data():
    url = 'http://127.0.0.1:5000/stream-items'  # Flask API endpoint
    messages = 0
    with requests.get(url, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    # Parse the JSON data from the SSE stream
                    data = json.loads(line.decode('utf-8').split('data: ')[1].strip())
                    # print(f"Received data: {data}")
                    publish_to_pubsub(data)
                    messages +=1 
                    print(f"messages sent: {messages}")
                    # time.sleep(0) 
while(True):
    subscribe_and_process_data()
    # subscribe_and_process_data2()
    # time.sleep()


