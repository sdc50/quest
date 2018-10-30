import types

class Metadata(types.SimpleNamespace):
    pass

    def as_dict(self):
        return self.__dict__