# -*- coding: utf-8 -*-

from pycommon.AbstractObject import AbstractObject, abstractproperty
from pycommon.utilites.class_property import classproperty
from pycommon.pyVmomiService import pyVmomiService
from models.ServiceProxy import ServiceProxy

from pycommon.logger import getLogger
_logger = getLogger("vCenterCommon")


class NamedEntryObject(AbstractObject):
    """
    Defines abstract named entry
    """
    def __init__(self, path="/", name="", uuid=None):
        """
        :param name: <str> name of entry
        """
        self.name = name
        self.path = path
        self.uuid = uuid

    @abstractproperty
    def type_name(cls): pass


class NamedEntry(NamedEntryObject):
    """
    Defines abstract named entry
    """
    def __init__(self, service_proxy, path="/", name="", uuid=None):
        super(NamedEntry, self).__init__(path, name, uuid)
        self.proxy = service_proxy

        self.obj = None

    def get_object(self):
        self.obj = self.proxy.performer.find_obj_by_path(self.proxy.si, self.path, self.name, self.type_name)
        return self.obj

    def get_object_by_uuid(self):
        if self.uuid:
            self.obj = self.proxy.performer.find_by_uuid(self.proxy.si, self.path, self.uuid)
        return self.obj


