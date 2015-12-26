from abc import ABCMeta, abstractmethod
from pycommon.AbstractObject import AbstractObject


class BaseCommand(AbstractObject):
    """base command"""

    @abstractmethod
    def execute(self):
        """This method should be overridden"""
