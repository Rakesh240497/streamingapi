from flask import Flask, Response
import json
from faker import Faker
import time

app = Flask(__name__)

# Initialize Faker instance
fake = Faker()

# Function to generate a single dummy item
def generate_dummy_item():
    item = {
        'id': fake.uuid4(),
        'name': fake.word(),
        'description': fake.sentence(),
        'price': round(fake.random_number(digits=2), 2),
        'category': fake.word(),
        'created_at': fake.date_time_this_year().isoformat()
    }
    return item

# Streaming route using SSE to stream data
@app.route('/stream-items', methods=['GET'])
def stream_items():
    def generate():
        while True:
            # Generate dummy data every 2 seconds
            item = generate_dummy_item()
            
            # Manually convert the item to a JSON string
            item_json = json.dumps(item)
            
            # Yield the data in SSE format
            yield f"data: {item_json}\n\n"
            # time.sleep()  # Simulate a delay to stream data every 2 seconds
    
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=False)
