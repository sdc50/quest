import pandas as pd

from .base import QuestEntity, db
from .collection import Collection
from .catalog_entry import CatalogEntry
from ..static import DatasetSource, DatasetStatus
from ..util import uuid, is_uuid, logger
from ..database import select_datasets

class Dataset(QuestEntity):
    """

    """
    db_entity = db.Dataset

    def __init__(self, catalog_entry, collection, source=None, display_name=None,
                 description=None, file_path=None, metadata=None, name=None):
        """Create a new dataset in a collection.

        Args:
            catalog_entry (string, Required):
                catalog_entry uri
            collection (string, Required):
                name of collection to create dataset in
            source (string, Optional, Default=None):
                type of the dataset such as timeseries or raster
            display_name (string, Optional, Default=None):
                display name for dataset
            description (string, Optional, Default=None):
                description of dataset
            file_path (string, Optional, Default=None):
                path location to save new dataset's data
            metadata (dict, Optional, Default=None):
                user defined metadata
            name (dict, Optional, Default=None):
                optionally pass in a UUID starting with d as name, otherwise it will be generated

        Returns:
            uri (string):
                uid of dataset
        """
        self._init(catalog_entry, collection, source, display_name,
              description, file_path, metadata, name)
        super().__init__()

    def _init(self, catalog_entry, collection, source=None, display_name=None,
              description=None, file_path=None, metadata=None, name=None, **kwargs):
        self._name = self._validate_name(name)
        self._collection = Collection.get(collection)
        self.catalog_entry = CatalogEntry.get(catalog_entry)
        self.source = source or DatasetSource.USER
        self.display_name = display_name or self.name
        self.description = description
        self.file_path = file_path
        self.metadata = metadata

    @property
    def name(self):
        return self._name

    @property
    def collection(self):
        return self._collection

    @property
    def donwload_options(self):
        pass

    @property
    def geometry(self):
        return self.catalog_entry.geometry

    def download(self):
        pass

    def move(self):
        pass

    def copy(self):
        pass

    def open(self):
        # TODO or should this be a data attribute?
        pass

    def as_dict(self):
        return {
            'name': self.name,
            'collection': self.collection.name,
            'catalog_entry': self.catalog_entry,
            'source': self.source,
            'display_name': self.display_name,
            'description': self.description,
            'file_path': self.file_path,
            'metadata': self.metadata,
        }


    def _validate_name(self, name):
        name = name or uuid('dataset')
        assert name.startswith('d') and is_uuid(name)
        return name

    @classmethod
    def _list(cls, select_func=None, filters=None, queries=None, **kwargs):
        # return select_datasets()
        datasets = select_datasets(select_func=select_func)
        datasets = pd.DataFrame(datasets)
        if not datasets.empty:
            datasets.set_index('name', inplace=True, drop=False)

        # if datasets.empty:
        #     if not expand and not as_dataframe:
        #         datasets = []
        #     elif not as_dataframe:
        #         datasets = {}
        #     return datasets

        if filters is not None:
            for k, v in filters.items():
                if k not in datasets.keys():
                    logger.warning('filter field {} not found, continuing'.format(k))
                    continue

                datasets = datasets.loc[datasets[k] == v]

        if queries is not None:
            for query in queries:
                datasets = datasets.query(query)

        datasets = list(datasets.to_dict(orient='index').values())

        return datasets

