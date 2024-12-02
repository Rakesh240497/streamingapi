import psutil
import time
import json
from flask import Flask, Response



app = Flask(__name__)

@app.route('/cpudata', methods=['GET'])
def monitor_system():
    try:
        while True:
            # Collect CPU usage
            cpu = psutil.cpu_percent(interval=1)
            
            # Try to collect CPU frequency, with fallback
            try:
                cpu_freq = psutil.cpu_freq()
                cpu_freq_data = {
                    "frequency_mhz": cpu_freq.current if cpu_freq else None
                }
            except FileNotFoundError:
                cpu_freq_data = {"frequency_mhz": "Unavailable"}

            # Collect Memory metrics
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()

            # Collect Disk metrics
            disk = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()

            # Collect Network metrics
            net_io = psutil.net_io_counters()

            # Collect Battery metrics (if applicable)
            battery = psutil.sensors_battery()

            # Prepare metrics dictionary
            system_metrics = {
                "cpu": {
                    "usage_percent": cpu,
                    **cpu_freq_data,  # Add CPU frequency info dynamically
                },
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used,
                    "free": memory.free,
                    "swap": {
                        "total": swap.total,
                        "used": swap.used,
                        "free": swap.free,
                        "percent": swap.percent,
                    },
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": disk.percent,
                    "io": {
                        "read_bytes": disk_io.read_bytes,
                        "write_bytes": disk_io.write_bytes,
                        "read_time": disk_io.read_time,
                        "write_time": disk_io.write_time,
                    },
                },
                "network": {
                    "bytes_sent": net_io.bytes_sent,
                    "bytes_received": net_io.bytes_recv,
                    "packets_sent": net_io.packets_sent,
                    "packets_received": net_io.packets_recv,
                },
                "battery": {
                    "percent": battery.percent if battery else None,
                    "secs_left": battery.secsleft if battery else None,
                    "power_plugged": battery.power_plugged if battery else None,
                }
            }

            # Convert to JSON and print
            json_metrics = json.dumps(system_metrics, indent=4)
            print(json_metrics)
            # time.sleep(1)  # Adjust the interval as needed

    except KeyboardInterrupt:
        print("Monitoring stopped.")

# Run the monitoring function
if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=False)
