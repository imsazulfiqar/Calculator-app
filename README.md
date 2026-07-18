# Modern Calculator App

A small FastAPI-based calculator application that serves a modern web UI and exposes a JSON API endpoint at `/api/calc`.

## Features

- Modern calculator UI served from a static folder
- JSON API endpoint for evaluating arithmetic expressions
- Supports addition, subtraction, multiplication, division, parentheses, decimal values, and `^` for exponentiation
- Uses FastAPI and Uvicorn for a lightweight Python web server

## Project Structure

- `learn.py` - main FastAPI application
- `static/index.html` - calculator frontend UI
- `static/` - static asset folder

## Setup

1. Install Python dependencies:

```bash
python3 -m pip install fastapi uvicorn
```

2. Run the application:

```bash
python3 learn.py
```

3. Open a browser and visit:

```text
http://127.0.0.1:8000/
```

## API

- `POST /api/calc`

Request body:

```json
{
  "expression": "2 + 3 * 4"
}
```

Response:

```json
{
  "expression": "2 + 3 * 4",
  "result": 14.0
}
```

## Notes

- The app validates expressions and returns HTTP 400 for invalid input.
- The UI sends expressions to `/api/calc` and renders the result.
