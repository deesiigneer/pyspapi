class City:
    def __init__(
        self,
        role=None,
        created_at=None,
        city_id=None,
        name=None,
        x_cord=None,
        z_cord=None,
        nether_x_cord=None,
        nether_z_cord=None,
        lane=None,
    ):
        self._role = role
        self._created_at = created_at
        self._city_id = city_id
        self._name = name 
        self._x_cord = x_cord
        self._z_cord = z_cord
        self._nether_x_cord = nether_x_cord
        self._nether_z_cord = nether_z_cord
        self._lane = lane

    @property
    def role(self):
        return self._role

    @property
    def created_at(self):
        return self._created_at

    @property
    def city_id(self):
        return self._city_id

    @property
    def x_cord(self):
        return self._x_cord

    @property
    def z_cord(self):
        return self._z_cord

    @property
    def nether_x_cord(self):
        return self._nether_x_cord

    @property
    def nether_z_cord(self):
        return self._nether_z_cord

    @property
    def lane(self):
        return self._lane

    def __repr__(self):
        return f"City(role={self.role}, created_at={self.created_at}, м={self.city_id}, x_cord={self.x_cord}, z_cord={self.z_cord}, nether_x_cord={self.nether_x_cord}, nether_z_cord={self.nether_z_cord}, lane={self.lane})"


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
    def __init__(self, account_id, username, minecraft_uuid, status, roles, created_at, cards, cities):
        self._id = account_id
        self._username = username
        self._minecraft_uuid = minecraft_uuid
        self._status = status
        self._roles = roles
        self._cities = [
            City(
                role=city["role"],
                created_at=city["createdAt"],
                id=city["city"]["id"],
                name=city["city"]["name"],
                x_cord=city["city"]["x"],
                z_cord=city["city"]["z"],
                nether_x_cord=city["city"]["netherX"],
                nether_z_cord=city["city"]["netherZ"],
                lane=city["city"]["lane"],
            )
            for city in cities
        ]
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
    def minecraft_uuid(self):
        return self._minecraft_uuid

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
        return f"Account(id={self.id}, username={self.username}, minecraft_uuid={self.minecraft_uuid}, status={self.status}, roles={self.roles}, cities={self.cities}, cards={self.cards}, created_at={self.created_at})"
