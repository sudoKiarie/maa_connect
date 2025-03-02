import streamlit as st
import requests

# Backend API URL
BASE_URL = "https://maa-connect-1.onrender.com"  # Update with your backend URL if deployed

st.title("Network Management Support")

# Fetch network topics from the backend
@st.cache_data
def get_network_topics():
    response = requests.get(f"{BASE_URL}/get_network_topics")
    if response.status_code == 200:
        return response.json()
    return {}

topics = get_network_topics()

# Sidebar for category selection
st.sidebar.header("Select a Network Topic")
selected_category = st.sidebar.radio("Categories", list(topics.keys()))

# Display questions for the selected category
if selected_category:
    st.subheader(f"{selected_category.replace('_', ' ').title()} Questions")
    selected_question = st.radio("Select a question", topics[selected_category])
    
    if st.button("Ask this question"):
        response = requests.post(f"{BASE_URL}/process_question", json={"question": selected_question})
        if response.status_code == 200:
            st.write("### Response:")
            st.write(response.json().get("reply", "No response received."))
        else:
            st.error("Failed to get a response. Try again later.")

# Custom question input
st.subheader("Ask a Custom Question")
custom_question = st.text_input("Enter your question:")
if st.button("Submit Custom Question") and custom_question:
    response = requests.post(f"{BASE_URL}/process_question", json={"question": custom_question})
    if response.status_code == 200:
        st.write("### Response:")
        st.write(response.json().get("reply", "No response received."))
    else:
        st.error("Failed to process your question.")

# Network diagnostic tools
st.sidebar.header("Network Tools")

if st.sidebar.button("Run Ping Test"):
    response = requests.get(f"{BASE_URL}/ping_test")
    if response.status_code == 200:
        st.sidebar.success(response.json().get("message"))
    else:
        st.sidebar.error("Ping test failed.")

if st.sidebar.button("Run Speed Test"):
    response = requests.get(f"{BASE_URL}/speed_test")
    if response.status_code == 200:
        speeds = response.json()
        st.sidebar.markdown(
            f"<p style='color: green; font-size: 18px;'>Download Speed: {speeds.get('download_speed')} Mbps</p>",
            unsafe_allow_html=True
        )

        st.sidebar.markdown(
            f"<p style='color: green; font-size: 18px;'>Upload Speed: {speeds.get('upload_speed')} Mbps</p>",
            unsafe_allow_html=True
        )
    else:
        st.sidebar.error("Speed test failed.")

if st.sidebar.button("Scan Network"):
    response = requests.get(f"{BASE_URL}/scan_network")
    if response.status_code == 200:
        devices = response.json().get("devices", [])
        st.sidebar.write("Connected Devices:")
        for device in devices:
            st.sidebar.write(f"- {device}")
    else:
        st.sidebar.error("Network scan failed.")

if st.sidebar.button("WiFi Diagnostic"):
    response = requests.get(f"{BASE_URL}/wifi_diagnostic")
    if response.status_code == 200:
        weak_signals = response.json().get("weak_signals", [])
        if weak_signals:
            st.sidebar.write("Weak WiFi Signals Detected:")
            for signal in weak_signals:
                st.sidebar.write(f"- {signal}")
        else:
            st.sidebar.success("No weak signals detected.")
    else:
        st.sidebar.error("WiFi diagnostic failed.")
