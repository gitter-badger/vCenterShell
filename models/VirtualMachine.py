# -*- coding: utf-8 -*-
"""
@see https://www.vmware.com/support/developer/converter-sdk/conv50_apireference/vim.vm.ConfigSpec.html
"""

from pycommon.pyVmomiService import *
from pycommon.utilites.class_property import classproperty
from models.NamedEntry import NamedEntry

# import vim.vm.device.VirtualDeviceSpec.Operation as OPERATION



from pycommon.logger import getLogger
_logger = getLogger("vCenterCommon")


class VirtualMachine(NamedEntry):
    def __init__(self, service_proxy, path, name="", uuid=None):
        super(VirtualMachine, self).__init__(service_proxy, path, name, uuid)

    @classproperty
    def type_name(cls):
        return pyVmomiService.VM

    def get_vm(self):
        return self.get_object()

    @staticmethod
    def task_remove_all_interfaces(virtual_machine):
        """
        @see https://www.vmware.com/support/developer/vc-sdk/visdk41pubs/ApiReference/vim.VirtualMachine.html#reconfigure
        :param virtual_machine: <vim.vm object>
        :return:
        """
        device_change = []
        for device in virtual_machine.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualEthernetCard):
                nicspec = vim.vm.device.VirtualDeviceSpec()
                nicspec.device = device
                nicspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
                device_change.append(nicspec)

        config_spec = vim.vm.ConfigSpec(deviceChange=device_change)
        task = virtual_machine.ReconfigVM_Task(config_spec)
        _logger.info("Virtual Machine remove ALL Interfaces task COMPOSED. Task: {}".format(task))
        return task

