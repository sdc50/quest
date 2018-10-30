import os
import pandas as pd

from .base import QuestEntity, db, db_session
from .project import Project
from ..database import select_collections

class Collection(QuestEntity):
    """

    """
    db_entity = db.Collection

    def __init__(self, name, display_name=None, description=None, metadata=None):
        """Create a new collection.

        Create a new collection by creating a new folder in project directory
        and adding collection metadata in project database.

        Args:
            name (string, Required):
                Name of the collection used in all quest function calls,must be unique. Will also be the folder name of the collection
            display_name (string, Optional, Default=None):
                display name for collection
            description (string, Optional, Default=None):
                description of collection
            metadata (dict, Optional, Default=None):
                user defined metadata

        Returns:
            collection (dict)
                details of the newly created collection
        """
        self._init(name, display_name, description, metadata)
        os.makedirs(self.path, exist_ok=True)
        super().__init__()


    def _init(self, name, display_name=None, description=None, metadata=None):
        self._name = self._validate_name(name)
        self.display_name = display_name or self.name
        self.description = description or ''
        self._project = Project.get_active_project()
        self.metadata = metadata

    @property
    def name(self):
        return self._name

    @property
    def project(self):
        return self._project

    @property
    def path(self):
        return os.path.join(self.project.path, self.name)

    @property
    @db_session()
    def datasets(self):
        from .dataset import Dataset
        # TODO is this what we want to do?
        datasets = list()
        db_instance = self.db_entity[self.name]
        db_datasets = db_instance.datasets
        for db_dataset in db_datasets:
            datasets.append(Dataset.get(db_dataset))
        return datasets


    def as_dict(self):
        return {
            'name': self.name,
            'display_name': self.display_name,
            'description': self.description,
            'metadata': self.metadata
        }

    def _validate_name(self, name):
        name = name.lower()
        try:
            self.db_instance
            raise ValueError('Collection %s already exists' % name)
        except ValueError:
            pass

        return name

    @classmethod
    def _list(cls, **kwargs):
        """Get available collections.

        Collections are folders on the local disk that contain downloaded or
        created data along with associated metadata.

        Args:
            expand (bool, Optional, Default=False):
                include collection details and format as dict
            as_dataframe (bool, Optional, Default=False):
                include collection details and format as pandas dataframe

        Returns:
            collections (list, dict, or pandas dataframe, Default=list):
                all available collections

        """
        return select_collections()