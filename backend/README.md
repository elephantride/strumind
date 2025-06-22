# StruMind Backend

StruMind is a SaaS structural engineering tool that provides advanced analysis, design, detailing, and BIM functionality.

## Features

- **Analysis Engine**: Linear, non-linear, P-delta, dynamic, and finite element analysis
- **Design Engine**: Steel, concrete, and composite design based on various design codes
- **Detailing Module**: Automatic detailing for fabrication
- **BIM Integration**: 3D BIM modeling and visualization

## Architecture

The backend is built with:

- **FastAPI**: Modern, high-performance web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Primary database
- **SQLite**: Optional lightweight storage

## Project Structure

```
backend/
  ├── app/
  │   ├── api/            # FastAPI route handlers
  │   ├── core/           # Analysis, design, detailing, BIM logic
  │   ├── models/         # SQLAlchemy models
  │   ├── schemas/        # Pydantic models for API
  │   ├── db/             # Database configuration
  │   └── utils/          # Helper utilities
  ├── main.py             # FastAPI entry point
  ├── requirements.txt    # Dependencies
  └── README.md           # Documentation
```

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL (or SQLite for development)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/strumind.git
   cd strumind/backend
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

5. Run the application:
   ```
   uvicorn main:app --reload
   ```

6. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

The API is organized into the following modules:

- `/api/v1/projects`: Project management
- `/api/v1/nodes`: Node definition
- `/api/v1/elements`: Element definition
- `/api/v1/materials`: Material properties
- `/api/v1/sections`: Section properties
- `/api/v1/loads`: Load definition
- `/api/v1/analysis`: Analysis control
- `/api/v1/design`: Design checks
- `/api/v1/detailing`: Detailing generation
- `/api/v1/bim`: BIM model management

## Development

### Database Migrations

We use Alembic for database migrations:

```
# Initialize migrations
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### Testing

Run tests with pytest:

```
pytest
```

## License

[Specify your license here]