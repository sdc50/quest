from abc import ABC, abstractmethod

import pandas as pd
import pony

from ..database import get_db, db_session
from .metadata import Metadata

db = get_db()

class QuestEntity(ABC):
    """

    """
    db_entity = None

    def __init__(self, name):
        self._name = name
        self._db_entity = None
        self._update_db()

    @abstractmethod
    def _init(self, *args, **kwargs):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        # return str(self.as_dict())
        return '<{}({})>'.format(self.__class__.__name__, self.display_name)

    @property
    def name(self):
        return self._name

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        metadata = metadata or dict()
        self._metadata = Metadata(**metadata)


    # def db_entity(cls):
    #     # if self._db_entity is None:
    #     #     db = get_db()
    #     #     self._db_entity = getattr(db, self.__class__.__name__)
    #     # return self._db_entity
    #     return None

    @property
    @db_session()
    def db_instance(self):
        try:
            db_instance = self.db_entity[self.name]
        except pony.orm.core.ObjectNotFound:
            raise ValueError('{} object with name {} does not exists.'.format(self.__class__.__name__, self.name))
        return db_instance

    @classmethod
    def get(cls, name):
        self = cls.__new__(cls)
        if isinstance(name, str):
            self._name = name
            db_instance = self.db_instance
        else:
            db_instance = name
        db_instance = db_instance.to_dict()
        del db_instance['updated_at']
        del db_instance['created_at']
        self._init(**db_instance)
        return self

    @classmethod
    def list(cls, expand=False, as_dataframe=False, **kwargs):
        entities = cls._list(**kwargs)
        import pdb; pdb.set_trace()
        if not expand and not as_dataframe:
            entities = [cls.get(e['name']) for e in entities]

        if as_dataframe:
            entities = pd.DataFrame.from_records(entities)

        return entities

    @classmethod
    @abstractmethod
    def _list(cls, **kwargs):
        """return a list of dictionaries with db data for entities"""
        pass

    @abstractmethod
    def as_dict(self):
        pass

    def _update_db(self):
        db = get_db()
        entity = getattr(db, self.db_entity)
        with db_session:
            entity(**self.as_dict())
