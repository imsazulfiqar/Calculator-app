from __future__ import annotations

import ast
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Create the FastAPI app instance that will serve the calculator UI and API.
app = FastAPI(title="Modern Calculator", version="1.0.0")

# Allow browser requests from any origin so the frontend can call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Find the folder that contains this script and the UI files.
# The UI lives in public/ because Vercel serves that folder as static files.
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "public"


# Define the expected JSON body for the calculator API.
class CalcRequest(BaseModel):
    expression: str


def evaluate_expression(expression: str) -> float:
    # Convert the UI's ^ symbol into Python's ** operator.
    normalized = expression.replace("^", "**")

    # Keep only characters that are safe for a simple math expression.
    cleaned = "".join(ch for ch in normalized if ch.isdigit() or ch in "+-*/(). ")
    if not cleaned:
        raise ValueError("Expression is empty")

    try:
        # Parse the expression into an abstract syntax tree.
        tree = ast.parse(cleaned, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid expression") from exc

    # Recursively evaluate the parsed expression tree.
    def _eval(node: ast.AST):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError("Division by zero")
                return left / right
            if isinstance(node.op, ast.Pow):
                return left**right
            raise ValueError("Unsupported operator")
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            if isinstance(node.op, ast.UAdd):
                return operand
            if isinstance(node.op, ast.USub):
                return -operand
            raise ValueError("Unsupported unary operator")
        raise ValueError("Unsupported expression")

    return _eval(tree)


# Serve the calculator UI at the root URL.
@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


# Accept a math expression from the browser and return the result as JSON.
@app.post("/api/calc")
def calculate(payload: CalcRequest):
    expression = payload.expression.strip()
    if not expression:
        raise HTTPException(status_code=400, detail="Expression is empty")

    try:
        result = evaluate_expression(expression)
    except (ValueError, ZeroDivisionError, SyntaxError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"expression": expression, "result": result}


# A simple GET endpoint to explain how to use the calculator API.
@app.get("/api/calc")
def calc_info():
    return {"message": "Send a POST request with an expression field to calculate results."}


# Run the app when this file is executed directly.
if __name__ == "__main__":
    uvicorn.run("learn:app", host="127.0.0.1", port=8000, reload=False)
