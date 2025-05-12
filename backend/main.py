from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware

from backend.database import get_db
from backend.crud import get_products
from backend.models import Product

from typing import List

app = FastAPI()

# Allow CORS (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/products", response_model=List[dict])
async def read_products(
    q: str = "",
    category: str = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    page: int = 1,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    try:
        products = await get_products(
            db, q, category, sort_by, sort_order, page, limit
        )
        return [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "category": p.category
            }
            for p in products
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))