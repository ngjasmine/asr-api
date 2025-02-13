#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "🚀 Setting up Python virtual environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 is not installed. Please install Python 3 and rerun this script."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🔹 Creating virtual environment..."
    python3 -m venv asr-api
else
    echo "✅ Virtual environment already exists. Skipping creation."
fi

# Activate virtual environment
echo "🔹 Activating virtual environment..."
source asr-api/bin/activate

# Upgrade pip
echo "🔹 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "🔹 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "✅ Setup complete! To activate the environment, run:"
echo "   source asr-api/bin/activate"
