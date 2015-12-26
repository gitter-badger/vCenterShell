# -*- coding: utf-8 -*-

from pycommon.pyVmomiService import pyVmomiService
from pycommon.logger import getLogger
_logger = getLogger("vCenterCommon")


class ServiceProxy(object):
    def __init__(self, service_performer, service_instance=None):
        self.service_performer = service_performer
        self.service_instance = service_instance

    def connect(self, host="localhost", username="", password="", port=443):
        self.service_instance = self.service_performer.connect(host, username, password, port)
        _logger.debug("vCenter Connection {}".format("SUCCESS" if self.service_instance else "ERROR"))

    @property
    def si(self):
        return self.service_instance

    @property
    def performer(self):
        return self.service_performer