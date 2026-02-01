class City:
    def __init__(
        self,
        city_id=None,
        name=None,
        x=None,
        z=None,
        nether_x=None,
        nether_z=None,
        lane=None,
        role=None,
        created_at=None,
    ):
        self._id = city_id
        self._name = name
        self._x = x
        self._z = z
        self._nether_x = nether_x
        self._nether_z = nether_z
        self._lane = lane
        self._role = role
        self._created_at = created_at

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def x(self):
        return self._x

    @property
    def z(self):
        return self._z

    @property
    def nether_x(self):
        return self._nether_x

    @property
    def nether_z(self):
        return self._nether_z

    @property
    def lane(self):
        return self._lane

    @property
    def role(self):
        return self._role

    @property
    def created_at(self):
        return self._created_at

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self._id!r}, name={self._name!r}, lane={self._lane!r}, role={self._role!r})>"


class Card:
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
        return f"<{self.__class__.__name__}(id={self._id!r}, name={self._name!r}, number={self._number!r})>"


class Account:
    def __init__(
        self,
        account_id,
        username,
        minecraftuuid,
        status,
        roles,
        created_at,
        cards,
        cities,
    ):
        self._id = account_id
        self._username = username
        self._minecraftuuid = minecraftuuid
        self._status = status
        self._roles = roles
        self._cities = [
            City(
                city_id=city["city"]["id"],
                name=city["city"]["name"],
                x=city["city"]["x"],
                z=city["city"]["z"],
                nether_x=city["city"]["netherX"],
                nether_z=city["city"]["netherZ"],
                lane=city["city"]["lane"],
                role=city["role"],
                created_at=city["createdAt"],
            )
            for city in cities
        ]
        self._cards = [
            Card(
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
    def minecraftuuid(self):
        return self._minecraftuuid

    @property
    def status(self):
        return self._status

    @property
    def roles(self):
        return self._roles

    @property
    def cities(self):
        return self._cities

    @property
    def cards(self):
        return self._cards

    @property
    def created_at(self):
        return self._created_at

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(id={self._id!r}, username={self._username!r}, status={self._status!r}, "
            f"roles={self._roles}, cities={self._cities}, cards={self._cards})>"
        )
