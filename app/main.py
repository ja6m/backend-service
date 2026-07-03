from fastapi import FastAPI, HTTPException, status

from app.models import Item, ItemCreate, ItemUpdate
from app.store import InMemoryItemStore

app = FastAPI(
    title="Backend Service",
    description="A simple FastAPI CRUD showcase backed by an in-memory store.",
    version="0.1.0",
)

store = InMemoryItemStore()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Welcome to the backend-service API. See /docs for details."}


@app.get("/items", response_model=list[Item])
def list_items() -> list[Item]:
    return store.list()


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item_in: ItemCreate) -> Item:
    return store.create(item_in)


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = store.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_in: ItemUpdate) -> Item:
    item = store.update(item_id, item_in)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    if not store.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
