from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware

from backend.cache import get_from_cache, set_to_cache, generate_cache_key
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
    cache_key = generate_cache_key("products", {
        "q": q,
        "category": category,
        "sort_by": sort_by,
        "sort_order": sort_order,
        "page": page,
        "limit": limit
    })

    cached = await get_from_cache(cache_key)
    if cached:
        return cached

    try:
        products = await get_products(
            db, q, category, sort_by, sort_order, page, limit
        )
        data = [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "category": p.category
            }
            for p in products
        ]

        await set_to_cache(cache_key, data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product Not Found")
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category
    }