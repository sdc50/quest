from .base import QuestEntity, db
from ..api.projects import get_active_project, _get_project_dir


class Project(QuestEntity):
    """

    """
    db_entity = db.Project

    def __init__(self, name):
        self._init()
        self._name = name

    def _init(self):
        self._path = None

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return _get_project_dir()

    @classmethod
    def get_active_project(cls):
        """Get an instance of the active project

        Returns:
            An instance of the active project
        """
        active_project_name = get_active_project()
        self = cls.__new__(cls)
        self.__init__(active_project_name)
        return self

    def as_dict(self):
        return self.__dict__

    @classmethod
    def _list(cls, **kwargs):
        pass

