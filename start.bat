@echo off
REM Weather App Startup Script for Windows
REM This script helps start both the backend and frontend servers

echo 🌤️  Weather App - PMA Tech Assessment
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 14+ first.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

REM Start Backend
echo 🚀 Starting Backend Server...
cd api

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Start the server in background
echo 🌐 Starting FastAPI server on http://localhost:8000
start /B python -m app.main

cd ..
echo ✅ Backend started

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend
echo 🚀 Starting Frontend Server...
cd frontend

REM Install dependencies
echo 📦 Installing Node.js dependencies...
npm install

REM Start the development server
echo 🌐 Starting React development server on http://localhost:3000
start /B npm start

cd ..
echo ✅ Frontend started

echo.
echo 🎉 Weather App is now running!
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo Press any key to stop both servers
pause >nul

REM Kill background processes
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM node.exe >nul 2>&1

echo ✅ Servers stopped
pause
