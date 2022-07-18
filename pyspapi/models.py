class _SPObject:
    """Возвращает словарь всех атрибутов экземпляра"""
    def to_dict(self) -> dict:
        return self.__dict__.copy()

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            self.__dict__
        )


class SPUserProfile(_SPObject):
    def __init__(self,
                 access: bool,
                 username: str,
                 ):
        self.access = access
        self.username = username


class _MojangObject:
    def to_dict(self) -> dict:
        """Возвращает словарь всех атрибутов экземпляра"""
        return self.__dict__.copy()

    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__,
            self.__dict__
        )


class MojangUserProfile(_MojangObject):
    def __init__(self, data: dict):
        self.timestamp = data['timestamp']
        self.id = data['profileId']
        self.name = data['profileName']

        self.is_legacy_profile = data.get('legacy')
        if self.is_legacy_profile is None:
            self.is_legacy_profile = False

        self.cape_url = None
        self.skin_url = None
        self.skin_model = 'classic'

        if data['textures'].get('CAPE'):
            self.cape_url = data['textures']['CAPE']['url']

        if data['textures'].get('SKIN'):
            self.skin_url = data['textures']['SKIN']['url']
            self.skin = data['textures']['SKIN']
            if data['textures']['SKIN'].get('metadata'):
                self.skin_model = 'slim'
