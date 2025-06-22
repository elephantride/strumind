#!/bin/bash

# Install backend dependencies
cd /workspace/Strumind/backend
pip install -r requirements.txt

# Install Playwright
pip install playwright
playwright install

# Set environment variables for SQLite (for testing)
export USE_SQLITE=true
export SQLITE_DB=strumind_test.db
export DEBUG=true
export PORT=8000

# Start the backend server
cd /workspace/Strumind
python backend/main.py &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Start the frontend
cd /workspace/Strumind
npm install
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
echo "Waiting for frontend to start..."
sleep 10

# Run the Playwright test
cd /workspace/Strumind
python tests/playwright/test_10_story_building.py

# Cleanup
kill $BACKEND_PID
kill $FRONTEND_PID

echo "Test completed!"