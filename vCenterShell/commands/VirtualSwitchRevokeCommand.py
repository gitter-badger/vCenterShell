# -*- coding: utf-8 -*-
"""
@see https://waffle.io/QualiSystems/vCenterShell/cards/5666b2aa0c076d2300052216 for initial info
"""

from pyVmomi import vim
from pycommon.pyVmomiService import *
import qualipy.scripts.cloudshell_scripts_helpers as helpers
from pycommon.common_collection_utils import first_or_default
# from models.VCenterConnectionDetails import VCenterConnectionDetails
# from pycommon.ResourceConnectionDetailsRetriever import ResourceConnectionDetailsRetriever
# from pycommon.pyVmomiService import pyVmomiService


from .VirtualSwitchCommon import VirtualSwitchCommandBase

from pycommon.logger import getLogger

_logger = getLogger("vCenterShell")


class VirtualSwitchRevokeCommand(VirtualSwitchCommandBase):

    def __init__(self,
                 pyvmomi_service,
                 revoker,
                 connection_retriever,
                 synchronous_task_waiter):
        super(VirtualSwitchRevokeCommand, self).__init__(pyvmomi_service,
                                                         connection_retriever,
                                                         synchronous_task_waiter)
        self.revoker = revoker

    def revoke_vm_from_vlan(self):
        resource_context = helpers.get_resource_context_details()
        inventory_path_data = self.connection_retriever.getVCenterInventoryPathAttributeData(resource_context)

        virtual_machine_path = inventory_path_data.vm_folder
        vm_name = inventory_path_data.vCenter_resource_name

        self.revoker.revoke(vm_name, virtual_machine_path)

    def execute(self):
        return self.revoke_vm_from_vlan()


