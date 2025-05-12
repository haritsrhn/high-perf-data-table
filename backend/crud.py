from sqlalchemy import select, desc, asc, or_
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Product

async def get_products(
    db: AsyncSession,
    q: str = "",
    category: str = None,
    sort_by: str = "id",
    sort_order: str = "asc",
    page: int = 1,
    limit: int = 50,
):
    offset = (page - 1) * limit
    stmt = select(Product)

    if q:
        stmt = stmt.where(or_(Product.name.ilike(f"%{q}%"), Product.category.ilike(f"%{q}%")))

    if category:
        stmt = stmt.where(Product.category == category)

    sort_column = getattr(Product, sort_by, Product.id)
    sort_func = asc if sort_order == "asc" else desc
    stmt = stmt.order_by(sort_func(sort_column))

    stmt = stmt.offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()