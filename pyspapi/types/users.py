class UserCards:
    def __init__(self, name, number):
        self._name: str = name
        self._number: str = number

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self._id!r}, name={self._name!r}, number={self._number!r})>"


class User:
    def __init__(self, username, uuid, cards):
        self._username: str = username
        self._uuid: str = uuid
        self._cards = [
            UserCards(
                name=card["name"],
                number=card["number"],
            )
            for card in cards
        ]

    @property
    def username(self):
        return self._username

    @property
    def uuid(self):
        return self._uuid

    @property
    def cards(self):
        return self._cards

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.__dict__)
