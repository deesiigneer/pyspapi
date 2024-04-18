class City:
    def __init__(
        self,
        city_id=None,
        name=None,
        description=None,
        x_cord=None,
        z_cord=None,
        is_mayor=None,
    ):
        self._id = city_id
        self._name = name
        self._description = description
        self._x_cord = x_cord
        self._z_cord = z_cord
        self._isMayor = is_mayor

    @property
    def id(self):
        return self._id

    @property
    def description(self):
        return self._description

    @property
    def name(self):
        return self._name

    @property
    def x_cord(self):
        return self._x_cord

    @property
    def z_cord(self):
        return self._z_cord

    @property
    def mayor(self):
        return self._isMayor

    def __repr__(self):
        return f"City(id={self.id}, name={self.name}, description={self.description}, x={self.x_cord}, z={self.z_cord}, is_mayor={self.mayor})"


class Cards:
    def __init__(self, card_id=None, name=None, number=None, color=None):
        self._id = card_id
        self._name = name
        self._number = number
        self._color = color

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number

    @property
    def color(self):
        return self._color

    def __repr__(self):
        return f"Card(id={self.id}, name={self.name}, number={self.number}, color={self.color})"


class Account:
    def __init__(self, account_id, username, status, roles, created_at, cards, city):
        self._id = account_id
        self._username = username
        self._status = status
        self._roles = roles
        self._city = City(**city) if city else None
        self._cards = [
            Cards(
                card_id=card["id"],
                name=card["name"],
                number=card["number"],
                color=card["color"],
            )
            for card in cards
        ]
        self._created_at = created_at

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def status(self):
        return self._status

    @property
    def roles(self):
        return self._roles

    @property
    def city(self):
        return self._city

    @property
    def cards(self):
        return self._cards

    @property
    def created_at(self):
        return self._created_at

    def __repr__(self):
        return f"Account(id={self.id}, username={self.username}, status={self.status}, roles={self.roles}, city={self.city}, cards={self.cards}, created_at={self.created_at})"
