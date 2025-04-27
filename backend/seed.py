import asyncio
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from .database import engine, Base, AsyncSessionLocal
from .models import Product

fake = Faker()

async def seed_products(n: int = 100_000):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute("DELETE FROM products")  # clean slate
        batch_size = 1000
        for i in range(0, n, batch_size):
            products = [
                Product(
                    name=fake.word(),
                    description=fake.sentence(),
                    price=round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
                    category=fake.word(),
                )
                for _ in range(batch_size)
            ]
            session.add_all(products)
            await session.commit()
            print(f"Inserted {i + batch_size} products")

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await seed_products()

if __name__ == "__main__":
    asyncio.run(main())