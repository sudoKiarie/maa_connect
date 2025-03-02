# Install compatible versions
!pip install --upgrade torch torchvision torchaudio transformers speedtest-cli sentencepiece accelerate gradio

import gradio as gr
from transformers import pipeline
import speedtest
import torch

# Clear GPU cache
torch.cuda.empty_cache()

# Load AI model
model_name = "google/flan-t5-large"
chatbot = pipeline("text2text-generation", model=model_name, device=0)

# Function to check network speed and troubleshoot
def check_network_speed(user_issue):
    if not user_issue.strip():
        return "⚠️ **Please enter a valid network issue!**"

    # Show loading indicator
    yield "⏳ **Analyzing network issue... Running speed test...**"

    # Run speed test
    st_obj = speedtest.Speedtest()
    download_speed = st_obj.download() / 1_000_000  # Convert to Mbps
    upload_speed = st_obj.upload() / 1_000_000      # Convert to Mbps
    ping_latency = st_obj.results.ping

    # **Prompt for AI model**
    prompt = f"""
A user is experiencing a network issue: "{user_issue}"

Network Speed Test Results:
- Download Speed: {download_speed:.2f} Mbps
- Upload Speed: {upload_speed:.2f} Mbps
- Ping: {ping_latency:.2f} ms

Provide exactly 5 different troubleshooting steps to help the user.
Each step must be unique, actionable, and relevant to the problem.
Avoid repeating steps or giving generic advice like "Check your internet".
"""

    # Show processing status
    yield f"⏳ **Analyzing speed test results... Generating troubleshooting steps...**"

    # Generate AI response
    response = chatbot(prompt, max_length=250, do_sample=True, temperature=0.5, num_return_sequences=1)

    # Final response
    yield (
        f"🔽 **Download Speed:** {download_speed:.2f} Mbps\n"
        f"🔼 **Upload Speed:** {upload_speed:.2f} Mbps\n"
        f"📶 **Ping Latency:** {ping_latency:.2f} ms\n\n"
        f"### 🔍 Troubleshooting Steps:\n{response[0]['generated_text']}"
    )

# Gradio UI with compact design
with gr.Blocks(theme=gr.themes.Base()) as iface:  # 🔹 Removes Gradio footer
    gr.Markdown("## 📡 Network Troubleshooting Chatbot")
    gr.Markdown("Enter your network issue, and the AI will diagnose the problem with a speed test and troubleshooting steps.")

    user_input = gr.Textbox(placeholder="Describe your network problem...", label="🔍 Enter Your Network Issue")
    diagnose_button = gr.Button("Diagnose", variant="primary")  # 🔹 Ensures proper button display

    output = gr.Markdown()  # 🔹 Output area

    diagnose_button.click(fn=check_network_speed, inputs=user_input, outputs=output)

# Run Gradio app
iface.launch()
