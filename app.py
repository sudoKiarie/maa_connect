from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import platform
import speedtest
import re
from utils.tinyllama_integration import TinyLlamaChatbot


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Network management topics for the chatbot
network_topics = {
    "router_issues": [
        "How do I reset my router?",
        "How do I change my WiFi password?",
        "Why does my internet connection keep dropping?",
        "How can I fix slow internet speeds?",
        "How do I update my router's firmware?",
        "What is port forwarding, and how do I set it up?",
        "How do I configure the IP address on my router?"
    ],
    "connectivity_problems": [
        "Why do I have no internet connection?",
        "Why is my internet connection intermittent?",
        "How do I fix issues with my network cable?",
        "How do I troubleshoot my modem?",
        "What is DNS configuration, and how can I fix it?",
        "Why am I having problems with my network adapter?"
    ],
    "network_security": [
        "How do I configure firewall settings?",
        "What is WiFi security mode, and how do I set it?",
        "How do I change the default credentials on my router?",
        "How can I block unknown devices from accessing my network?",
        "What is MAC address filtering, and how do I enable it?",
        "How do I set up a VPN on my network?"
    ],
    "device_management": [
        "How do I add a new device to my network?",
        "How do I remove a device from my network?",
        "How do I reserve an IP address for a specific device?",
        "How can I allocate bandwidth to specific devices?",
        "How do I prioritize certain devices on my network?",
        "How can I view a network map of connected devices?"
    ],
    "advanced_networking": [
        "What is subnet configuration, and how do I set it up?",
        "How do I set up VLANs on my network?",
        "What is network segmentation, and how do I implement it?",
        "What is Quality of Service (QoS), and how do I configure it?",
        "How do I enable bridge mode on my router?",
        "How do I set up multiple access points for better coverage?"
    ],
    "troubleshooting_tools": [
        "How do I perform a ping test?",
        "What is traceroute, and how do I use it?",
        "How can I run a speed test to check my internet?",
        "What is network diagnostic mode, and how can I use it?",
        "How do I analyze packet loss on my network?",
        "How do I check the signal strength of my WiFi?"
    ]
}

@app.route('/get_network_topics', methods=['GET'])
def get_network_topics():
    """
    Endpoint to retrieve network management topics.
    """
    return jsonify(network_topics)

@app.route('/process_question', methods=['POST'])
def process_question():
    """
    Endpoint to process a question from the frontend using the TinyLlama model.
    """
    data = request.get_json()
    question = data.get('question')
    print(f"Received question: {question}")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        # Call the TinyLlama model to generate a response
        networkbot = TinyLlamaChatbot()
        response = networkbot.generate_response(question)
        return jsonify({"reply": response})
    except Exception as e:
        print(f"Error during TinyLlama processing: {e}")
        return jsonify({"error": "Failed to process the question. Please try again later."}), 500

@app.route('/ping_test', methods=['GET', 'POST'])
def ping_test():
    """
    Endpoint to perform a ping test and return latency.
    """
    target = request.args.get('target', '8.8.8.8')

    # Run the ping command with a timeout of 4 pings
    result = subprocess.run(["ping", "-c", "4", target], capture_output=True, text=True)

    if result.returncode == 0:
        # Extract latency information from the ping output
        # The output format is similar to: "rtt min/avg/max/mdev = 12.006/13.473/16.155/1.629 ms"
        ping_output = result.stdout
        latency_match = re.search(r'rtt min/avg/max/mdev = (\d+\.\d+/\d+\.\d+/\d+\.\d+/\d+\.\d+) ms', ping_output)

        if latency_match:
            latency = latency_match.group(1)  # The min/avg/max/mdev latency values
            return jsonify(status="success", message=f"Internet is working! The latency is {latency}.")
        else:
            return jsonify(status="error", message="Unable to parse latency information!")
    else:
        return jsonify(status="error", message="Internet connection is down!")

@app.route('/speed_test', methods=['GET', 'POST'])
def speed_test():
    """ 
    Endpoint to perform a speed test.
    """
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1_000_000  # Convert from bits to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert from bits to Mbps
        
        return jsonify(download_speed=f"{download_speed:.2f}", upload_speed=f"{upload_speed:.2f}")
    except Exception as e:
        return jsonify(error="Error: Could not perform speed test. Please try again later."), 500

@app.route('/scan_network', methods=['GET'])
def scan_network():
    """
    Scan the local network and list connected devices.
    """
    try:
        devices = []
        if platform.system() == "Windows":
            output = subprocess.check_output("arp -a", shell=True).decode()
            devices = re.findall(r"(\d+\.\d+\.\d+\.\d+)", output)  # Extract IPs
        else:
            output = subprocess.check_output("sudo arp-scan -l", shell=True).decode()
            devices = re.findall(r"(\d+\.\d+\.\d+\.\d+)", output)

        return jsonify(devices=devices)
    except Exception as e:
        return jsonify(error="Error: Could not scan the network."), 500

@app.route('/wifi_diagnostic', methods=['GET'])
def wifi_diagnostic():
    """
    Run Wi-Fi diagnostics (signal strength, speed, and network name).
    """
    try:
        wifi_info = {}
        
        if platform.system() == "Windows":
            output = subprocess.check_output("netsh wlan show interfaces", shell=True).decode()
            ssid = re.search(r"SSID\s*:\s(.+)", output)
            signal = re.search(r"Signal\s*:\s(\d+)%", output)

            wifi_info["SSID"] = ssid.group(1) if ssid else "Unknown"
            wifi_info["Signal Strength (%)"] = signal.group(1) if signal else "Unknown"
        
        else:  # Linux/macOS
            output = subprocess.check_output("iwconfig", shell=True).decode()
            ssid = re.search(r'ESSID:"(.+?)"', output)
            signal = re.search(r"Signal level=(-\d+)", output)

            wifi_info["SSID"] = ssid.group(1) if ssid else "Unknown"
            wifi_info["Signal Strength (dBm)"] = signal.group(1) if signal else "Unknown"

        return jsonify(wifi_info=wifi_info)
    except Exception as e:
        return jsonify(error="Error: Could not perform Wi-Fi diagnostic."), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
