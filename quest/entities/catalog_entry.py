import pandas as pd

from .base import QuestEntity
from ..api import get_metadata, search_catalog, get_services

class CatalogEntry(QuestEntity):
    """

    """
    def __init__(self):
        pass

    def _init(self, name):
        self.__dict__ = get_metadata(name)[name]
        self._name = self.__dict__.pop('name')

    def as_dict(self):
        d = self.__dict__.copy()
        d['name'] = d.pop('_name')
        return d

    @classmethod
    def get(cls, catalog_entry):
        self = cls.__new__(cls)
        self._init(catalog_entry)


        # if not isinstance(catalog_entry, pd.DataFrame):
        #     catalog_entry = get_metadata(catalog_entry, as_dataframe=True)
        # try:
        #     catalog_entry = catalog_entry['name'][0]
        # except IndexError:
        #     raise ValueError('{} object with name {} does not exists.'.format(self.__class__.__name__, self.name))
        return self

    @classmethod
    def _list(cls, **kwargs):
        kwargs.setdefault('uris', get_services())
        return cls.search(**kwargs)

    @classmethod
    def search(cls, **kwargs):
        kwargs.update(expand=True)
        return list(search_catalog(**kwargs).values())