class SPUser:
    def __init__(self, data: dict):
        self.__data = data

    @property
    def access(self) -> bool:
        return True if self.__data['username'] is not None else False

    def __repr__(self):
        return self.__data['username']


class MojangProfile:
    def __init__(self, data: dict):
        self.__data = data
        self.skin = Skin(data)

    @property
    def id(self) -> str:
        return self.__data['profileId']

    @property
    def timestamp(self):
        return self.__data['timestamp']

    def __repr__(self):
        return self.__data['profileName']


class Skin:
    def __init__(self, data: dict):
        self.__data = data

    @property
    def url(self) -> str:
        return self.__data['textures']['SKIN']['url']

    @property
    def cape_url(self) -> str:
        return self.__data['textures']['CAPE']['url']

    @property
    def model(self) -> str:
        return 'classic' if self.__data['textures']['SKIN'].get('metadata') is None else 'slim'

    def __repr__(self):
        return str(self.__data['textures']['SKIN'])


class UsernameToUUID:
    def __init__(self, data: dict):
        self.__data = data

    @property
    def id(self):
        return self.__data['id']

    @property
    def name(self):
        return self.__data['name']

    def __repr__(self):
        return str(self.__data['id'])
