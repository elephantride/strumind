# StruMind - Structural Engineering SaaS Platform

StruMind is a comprehensive SaaS structural engineering tool that combines the capabilities of Tekla, ETABS, and STAAD.Pro into a single, powerful platform.

## Features

- **Advanced Analysis Engine**: Linear, non-linear, P-delta, dynamic, and finite element analysis
- **Advanced Design Engine**: Steel, concrete, and composite design based on various design codes
- **Automatic Detailing**: Generate fabrication-ready drawings and connection details
- **3D BIM Integration**: Seamless 3D modeling and visualization
- **Modern Web Interface**: React-based frontend with intuitive controls

## Architecture

- **Frontend**: React + Tailwind CSS
- **Backend**: Python + FastAPI
- **Database**: PostgreSQL (primary), SQLite (optional)

## Project Structure

```
strumind/
├── backend/               # Python FastAPI backend
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core functionality
│   │   ├── models/        # Database models
│   │   ├── schemas/       # API schemas
│   │   ├── db/            # Database configuration
│   │   └── utils/         # Utilities
│   ├── main.py            # Entry point
│   └── requirements.txt   # Dependencies
├── client/                # React frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   ├── hooks/         # Custom hooks
│   │   └── lib/           # Utilities
│   └── package.json       # Dependencies
└── tests/                 # Tests
    └── playwright/        # End-to-end tests
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- PostgreSQL (optional, SQLite can be used for development)

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   # For PostgreSQL
   export POSTGRES_SERVER=localhost
   export POSTGRES_USER=postgres
   export POSTGRES_PASSWORD=postgres
   export POSTGRES_DB=strumind
   export POSTGRES_PORT=5432
   
   # For SQLite (development)
   export USE_SQLITE=true
   export SQLITE_DB=strumind.db
   
   # Debug mode
   export DEBUG=true
   ```

5. Run the backend:
   ```
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the client directory:
   ```
   cd client
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the frontend:
   ```
   npm run dev
   ```

4. Access the application at http://localhost:5173

## Testing

### Running End-to-End Tests

We use Playwright for end-to-end testing:

1. Install Playwright:
   ```
   pip install playwright
   playwright install
   ```

2. Run the test script:
   ```
   ./tests/run_tests.sh
   ```

This will:
- Start the backend and frontend servers
- Run the 10-story building test
- Record a video of the test execution
- Save screenshots of key steps

## API Documentation

When the backend is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc