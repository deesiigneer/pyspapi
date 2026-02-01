class Item:
    def __init__(self, name: str, count: int, price: int, comment: str):
        self._name = name
        self._count = count
        self._price = price
        self._comment = comment

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return f"<{self.__class__.__name__}(name={self._name!r}, count={self._count!r}, price={self._price!r}, comment={self._comment!r})>"

    def to_json(self):
        return {
            "name": self._name,
            "count": self._count,
            "price": self._price,
            "comment": self._comment,
        }
