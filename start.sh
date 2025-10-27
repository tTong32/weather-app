#!/bin/bash

# Weather App Startup Script
# This script helps start both the backend and frontend servers

echo "🌤️  Weather App - PMA Tech Assessment"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Function to start backend
start_backend() {
    echo "🚀 Starting Backend Server..."
    cd api
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "📦 Creating virtual environment..."
        python -m venv venv
    fi
    
    # Activate virtual environment
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # Install dependencies
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Start the server
    echo "🌐 Starting FastAPI server on http://localhost:8000"
    python -m app.main &
    BACKEND_PID=$!
    
    cd ..
    echo "✅ Backend started with PID: $BACKEND_PID"
}

# Function to start frontend
start_frontend() {
    echo "🚀 Starting Frontend Server..."
    cd frontend
    
    # Install dependencies
    echo "📦 Installing Node.js dependencies..."
    npm install
    
    # Start the development server
    echo "🌐 Starting React development server on http://localhost:3000"
    npm start &
    FRONTEND_PID=$!
    
    cd ..
    echo "✅ Frontend started with PID: $FRONTEND_PID"
}

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo "✅ Servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start both servers
start_backend
sleep 3
start_frontend

echo ""
echo "🎉 Weather App is now running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait
