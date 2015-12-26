# -*- coding: utf-8 -*-
"""
@see https://waffle.io/QualiSystems/vCenterShell/cards/5666b2aa0c076d2300052216 for initial info

@see https://www.vmware.com/support/developer/vc-sdk/visdk41pubs/ApiReference/vim.DistributedVirtualSwitch.html
"""

from pyVmomi import vim
from pycommon.pyVmomiService import *

from models.ServiceProxy import ServiceProxy
from models.VirtualMachine import VirtualMachine
from .VirtualSwitchCommon import VirtualSwitchCommandBase

from pycommon.logger import getLogger
_logger = getLogger("vCenterShell")


class VirtualSwitchFromMachineRevoker(VirtualSwitchCommandBase):

    def __init__(self,
                 pyvmomi_service,
                 connection_retriever,
                 synchronous_task_waiter):
        super(VirtualSwitchFromMachineRevoker, self).__init__(pyvmomi_service,
                                                              connection_retriever,
                                                              synchronous_task_waiter)

    def execute(self):
        pass

    def revoke(self, vm_name, virtual_machine_path):
        if not self.is_vcenter_connected():
            self.vcenter_connect(self.get_connection_details(vm_name))

        _logger.debug("Revoking ALL Interfaces from VM '{}'".format(vm_name))
        machine = VirtualMachine(ServiceProxy(self.pyvmomi_service, self.si), virtual_machine_path, vm_name, vm_uuid)
        vm = machine.get_vm()
        task = VirtualMachine.task_remove_all_interfaces(vm)
        logger.info("Virtual Machine remove ALL Interfaces task STARTED")
        return self.synchronous_task_waiter.wait_for_task(task)


