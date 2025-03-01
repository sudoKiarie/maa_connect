from flask import Flask, jsonify, request
from ping3 import ping
import speedtest
import random

app = Flask(__name__)

@app.route('/ping_test')
def ping_test():
    target = request.args.get('target', '8.8.8.8')
    latency = ping(target)
    if latency:
        return jsonify(status="success", message=f"Internet is working! The latency is {latency:.2f} ms.")
    else:
        return jsonify(status="error", message="Internet connection is down!")

@app.route('/speed_test')
def speed_test():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Convert from bits to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert from bits to Mbps
    return jsonify(download_speed=f"{download_speed:.2f}", upload_speed=f"{upload_speed:.2f}")

@app.route('/scan_network')
def scan_network():
    # Example of connected devices, in a real scenario, scan your local network
    connected_devices = ["Teacher laptop (192.168.1.101)", "Student laptop (192.168.1.102)", "Printer (192.168.1.103)"]
    return jsonify(devices=connected_devices)

@app.route('/wifi_diagnostic')
def wifi_diagnostic():
    weak_signals = random.choices(["Linksys", "Netgear", "Belkin"], k=3)
    if weak_signals:
        return jsonify(weak_signals=weak_signals)
    else:
        return jsonify(weak_signals=[])

if __name__ == "__main__":
    app.run(debug=True)
