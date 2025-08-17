# from typing import Union
# from fastapi import FastAPI
# from pydantic import BaseModel
from fastapi import FastAPI, Depends
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session, init_db
from models import Item

app = FastAPI()

# FastAPI code is mixing Pydantic models and SQLModel models, and you are trying to add a Pydantic Item to the database. That won’t work—SQLModel expects an SQLModel class instance, not a Pydantic BaseModel


# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


@app.on_event("startup")
async def on_startup():
    await init_db()

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

@app.post("/items/")
async def create_item(item: Item, session: AsyncSession = Depends(get_session)):
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item
    

@app.get("/items/")
async def read_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Item))
    items = result.scalars().all()
    return items


# @app.get("/")
# async def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}
