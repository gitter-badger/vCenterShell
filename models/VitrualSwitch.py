# -*- coding: utf-8 -*-
"""
@see https://waffle.io/QualiSystems/vCenterShell/cards/5666b2aa0c076d2300052216 for initial info

"""

from pycommon.pyVmomiService import *
from pycommon.utilites.class_property import classproperty
from models.NamedEntry import NamedEntry

from pycommon.logger import getLogger
_logger = getLogger("vCenterCommon")


class VirtualSwitch(NamedEntry):
    def __init__(self, service_proxy, path, name="", uuid=None):
        super(VirtualSwitch, self).__init__(service_proxy, path, name, uuid)

    @classproperty
    def type_name(cls):
        return pyVmomiService.Network

    def get_switch(self):
        return self.get_object()

    def task_destroy(self):
        pass
        # switch = self.get_switch()
        # if switch.portgroup:
        #     for group in switch.portgroup:
        #         group.config.
        #     pass
        # DVPortgroupConfigSpec
        # task = switch.ReconfigureDVPort_Task([])
        # _logger.info("Virtual Switch Destroy task COMPOSED. Task: {}".format(task))
        # return task



    @staticmethod
    def create_port_group(dv_port_name, spec, vlan_id, ports_number=32, inherited=False, mac_change=False):
        """
        Create Port Group
        :param dv_port_name: <str> Port Name
        :param spec:
        :param vlan_id:
        :param ports_number: <int>
        :return:
        """
        dv_pg_spec = vim.dvs.DistributedVirtualPortgroup.ConfigSpec()
        dv_pg_spec.name = dv_port_name
        dv_pg_spec.numPorts = ports_number
        dv_pg_spec.type = vim.dvs.DistributedVirtualPortgroup.PortgroupType.earlyBinding

        dv_pg_spec.defaultPortConfig = vim.dvs.VmwareDistributedVirtualSwitch.VmwarePortConfigPolicy()
        dv_pg_spec.defaultPortConfig.securityPolicy = vim.dvs.VmwareDistributedVirtualSwitch.SecurityPolicy()

        dv_pg_spec.defaultPortConfig.vlan = spec
        dv_pg_spec.defaultPortConfig.vlan.vlanId = vlan_id
        dv_pg_spec.defaultPortConfig.securityPolicy.allowPromiscuous = vim.BoolPolicy(value=True)
        dv_pg_spec.defaultPortConfig.securityPolicy.forgedTransmits = vim.BoolPolicy(value=True)

        dv_pg_spec.defaultPortConfig.vlan.inherited = inherited
        dv_pg_spec.defaultPortConfig.securityPolicy.macChanges = vim.BoolPolicy(value=mac_change)
        dv_pg_spec.defaultPortConfig.securityPolicy.inherited = inherited

        return dv_pg_spec


    @staticmethod
    def task_attach_port_group(dv_switch, port_group):
        """
        Create Port Group
        :param dv_switch: <vim.DistributedVirtualSwitch> see https://www.vmware.com/support/developer/converter-sdk/conv60_apireference/vim.DistributedVirtualSwitch.html#reconfigurePort
        :param dv_port_name: <str> Port Name
        :param spec:
        :param vlan_id:
        :return:
        """

        task = dv_switch.AddDVPortgroup_Task([port_group])

        _logger.info(u"DV Port Group Task Successfully created for name '{}'".format(port_group.name))

        return task
