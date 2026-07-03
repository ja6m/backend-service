from itertools import count

from app.models import Item, ItemCreate, ItemUpdate


class InMemoryItemStore:
    """A minimal thread-unsafe in-memory store, sufficient for demo purposes."""

    def __init__(self) -> None:
        self._items: dict[int, Item] = {}
        self._id_counter = count(1)

    def list(self) -> list[Item]:
        return list(self._items.values())

    def get(self, item_id: int) -> Item | None:
        return self._items.get(item_id)

    def create(self, item_in: ItemCreate) -> Item:
        item_id = next(self._id_counter)
        item = Item(id=item_id, **item_in.model_dump())
        self._items[item_id] = item
        return item

    def update(self, item_id: int, item_in: ItemUpdate) -> Item | None:
        existing = self._items.get(item_id)
        if existing is None:
            return None
        updated = existing.model_copy(update=item_in.model_dump(exclude_unset=True))
        self._items[item_id] = updated
        return updated

    def delete(self, item_id: int) -> bool:
        return self._items.pop(item_id, None) is not None

    def clear(self) -> None:
        self._items.clear()
        self._id_counter = count(1)
