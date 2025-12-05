#!/bin/bash
# Setup script for Advanced GenAI Pipeline

echo "🚀 Setting up Advanced GenAI Pipeline..."
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download spaCy models
echo ""
echo "Downloading spaCy language models..."
python -m spacy download en_core_web_sm
python -m spacy download de_core_news_sm

# Create directory structure
echo ""
echo "Creating directory structure..."
python setup_directories.py

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cat > .env << EOF
# OpenAI API Configuration
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your-api-key-here
EOF
    echo "⚠️  Please edit .env and add your OpenAI API key!"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Place HTML files in the data/ directory"
echo "3. Place benchmark PDF in the benchmark/ directory"
echo "4. Run: source venv/bin/activate"
echo "5. Follow the pipeline steps in README.md"

