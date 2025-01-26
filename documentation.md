# Network Management Troubleshooting Project

This project integrates a Flask backend with a React frontend for network management troubleshooting. Here's a breakdown of the key components:

## app.py (Flask Backend)

- **Flask app**: The Flask app is initialized, and CORS (Cross-Origin Resource Sharing) is enabled for cross-origin requests, making it compatible with the React frontend.
  
- **Network topics**: A dictionary of predefined network management topics (e.g., router issues, connectivity problems) is provided through the `/get_network_topics` endpoint.

- **Question Processing**: The `/process_question` endpoint receives a question from the frontend, processes it (currently, it returns a placeholder response), and sends it back.

### Network Tests:
- **Ping test (`/ping_test`)**: Pings a target (default is Google's DNS server 8.8.8.8) to check network connectivity.
- **Speed test (`/speed_test`)**: Uses the `speedtest` library to check download and upload speeds.
- **Network scan (`/scan_network`)**: Returns a list of connected devices (simulated for this example).
- **Wi-Fi diagnostic (`/wifi_diagnostic`)**: Simulates weak Wi-Fi signal diagnostics by returning a list of weak signal networks.

## index.html (Frontend)

- **React app**: A React app is embedded in the HTML file to handle the frontend logic.

### State management:
- **networkTopics**: Stores network topics fetched from the backend.
- **selectedCategory**: Stores the category selected by the user.
- **selectedQuestion**: Stores the question selected from the category.
- **customQuestion**: Stores a custom question typed by the user.

### Fetching data:
- On page load, the app fetches network topics from the backend and stores them in the state.

### Handling user interaction:
- The user selects a category or question, and the question is sent to the backend for processing.
- The user can also type a custom question and submit it to the backend.
- **Troubleshooting button**: Redirects the user to the network diagnostic page (`diagnostic.html`).

## diagnostic.html (Network Troubleshooting Page)

- **Diagnostic UI**: This page provides buttons for running different network diagnostics like ping tests, speed tests, network scans, and Wi-Fi diagnostics.
  
- **Results**: Displays success or error messages based on the results of each diagnostic.





