class Item:
    def __init__(self, name: str, count: int, price: int, comment: str):
        self._name = name
        self._count = count
        self._price = price
        self._comment = comment

    @property
    def name(self):
        return self._name

    def to_json(self):
        return {
            "name": self._name,
            "count": self._count,
            "price": self._price,
            "comment": self._comment
        }
