# AntiGravity

AntiGravity is an all-in-one housing application designed to help you find and track housing listings in the Netherlands, with integrated travel time calculations and budget filtering.

## Project Structure

The project is divided into two main components:

- **[backend](./backend)**: FastAPI server that handles web scraping, database storage (MongoDB), and travel time calculations using OpenRouteService and NS APIs.
- **[frontend](./frontend)**: React + Vite application providing a modern UI for browsing and filtering house listings.

## Quick Start

### 1. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # Or manually install FastAPI, Uvicorn, Motor, etc.
python main.py
```
*Make sure to configure your `.env` file in the backend directory.*

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Features

- **Housing Hub**: All-in-one interface for Dutch housing listings.
- **Multi-Source Scraping**: Integration with popular Dutch housing sites (Funda, VerhuurtBeter, etc.).
- **Smart Filtering**: Filter by budget and travel duration to a specific target location.
- **Modern UI**: Responsive design with liquid micro-interactions.

## Documentation

For more detailed instructions, see the individual READMEs:
- [Backend Documentation](./backend/README.md)
- [Frontend Documentation](./frontend/README.md)
