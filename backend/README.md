# AntiGravity Backend

FastAPI backend for the AntiGravity all-in-one housing app.

## Prerequisites

- Python 3.10+
- MongoDB (running locally or a connection string)
- API Keys for:
    - OpenRouteService (Travel times)
    - NS (Dutch Railways - for station data)

## Setup

1. **Environment Variables**:
   Create a `.env` file in this directory based on the configuration required:
   ```env
   PORT=
   MONGODB_URI=
   DB_NAME=
   ORS_API_KEY=
   NS_API_KEY=
   TARGET_LOCATION_LAT=
   TARGET_LOCATION_LON=
   ```

2. **Installation**:
   It is recommended to use a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install fastapi uvicorn motor python-dotenv motor requests funda-scraper
   ```
   *(Note: Ensure all dependencies from imports in main.py are installed)*

## Running the Server

Start the FastAPI server with:
```bash
python main.py
```
The server will be available at `http://localhost:8000`.

## API Endpoints

- `GET /`: Welcome message
- `GET /health`: Health check
- `POST /scrape?city={city}`: Trigger housing scrapers for a specific city
- `GET /houses`: Get list of houses with optional filters:
    - `max_budget`: Maximum monthly rent
    - `max_duration`: Maximum travel duration in minutes
- `POST /test-distance`: Test travel data calculation
