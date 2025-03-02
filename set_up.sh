#!/bin/bash

# Install system dependencies
sudo apt-get update
sudo apt-get install -y wireless-tools

# Install Python dependencies
pip install -r requirements.txt
