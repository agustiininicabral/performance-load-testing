from fastapi import FastAPI, Query
from pydantic import BaseModel, Field


app = FastAPI(
    title="Load Testing Demo API",
    description="Deterministic local target service for Locust performance scenarios.",
    version="1.0.0",
)

PRODUCTS = [
    {"id": i, "name": f"Product {i:03d}", "category": ("electronics", "home", "books", "sports")[i % 4], "price": round(10 + i * 2.35, 2)}
    for i in range(1, 101)
]


class ComputeRequest(BaseModel):
    iterations: int = Field(default=1000, ge=1, le=50000)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/products")
def products(limit: int = Query(default=20, ge=1, le=100)) -> list[dict]:
    return PRODUCTS[:limit]


@app.post("/compute")
def compute(payload: ComputeRequest) -> dict[str, int]:
    checksum = 0
    for index in range(payload.iterations):
        checksum = (checksum * 31 + index) % 1_000_003
    return {"iterations": payload.iterations, "checksum": checksum}
