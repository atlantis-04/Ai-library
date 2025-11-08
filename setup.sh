#!/bin/bash

echo "🚀 Setting up AI Library System..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Seed database
echo "🌱 Seeding database with sample data..."
python seed_data.py

echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  streamlit run app.py"
