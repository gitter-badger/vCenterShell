from unittest import TestCase
from mock import Mock, MagicMock
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import uuid

from vCenterShell.commands.VirtualMachinePortGroupConfigurer import VirtualMachinePortGroupConfigurer
from vCenterShell.commands.DvPortGroupCreator import DvPortGroupCreator
from vCenterShell.models.VCenterConnectionDetails import VCenterConnectionDetails
from tests.testCredentials import TestCredentials
from vCenterShell.commands.VirtualSwitchToMachineConnector import *


class TestVirtualSwitchToMachineConnector(TestCase):
    def test_connect(self):
        # Arrange
        si = Mock()

        py_vmomi_service = Mock()
        py_vmomi_service.connect = Mock(return_value=si)

        resource_connection_details_retriever = Mock()
        dv_port_group_creator = MagicMock()
        virtual_machine_port_group_configurer = MagicMock()
        virtual_switch_to_machine_connector = VirtualSwitchToMachineConnector(py_vmomi_service,
                                                                              resource_connection_details_retriever,
                                                                              dv_port_group_creator,
                                                                              virtual_machine_port_group_configurer)

        virtual_machine_path = 'ParentFlder\\ChildFolder'
        virtual_machine_name = 'MachineName'
        vm_uuid = uuid.UUID('{12345678-1234-5678-1234-567812345678}')
        port_group_path = 'QualiSB'
        dv_switch_path = 'QualiSB'
        dv_switch_name = 'dvSwitch'
        dv_port_name = 'dv_port_name'

        # Act
        virtual_switch_to_machine_connector.connect(virtual_machine_name, dv_switch_path, dv_switch_name,
                                                    dv_port_name, virtual_machine_path, vm_uuid,
                                                    port_group_path)

        # Assert
        dv_port_group_creator.create_dv_port_group.assert_called_with(dv_port_name, dv_switch_name, dv_switch_path, si)
        virtual_machine_port_group_configurer.configure_port_group_on_vm.assert_called_with(si, virtual_machine_path,
                                                                                            vm_uuid,
                                                                                            port_group_path,
                                                                                            dv_port_name)

    def integrationtest(self):
        resource_connection_details_retriever = Mock()
        credentials = TestCredentials()
        resource_connection_details_retriever.connection_details = Mock(
                return_value=VCenterConnectionDetails(credentials.host, credentials.username, credentials.password))
        py_vmomi_service = pyVmomiService(SmartConnect, Disconnect)
        synchronous_task_waiter = SynchronousTaskWaiter()
        dv_port_group_creator = DvPortGroupCreator(py_vmomi_service, synchronous_task_waiter)
        virtual_machine_port_group_configurer = VirtualMachinePortGroupConfigurer(py_vmomi_service,
                                                                                  synchronous_task_waiter)
        virtual_switch_to_machine_connector = VirtualSwitchToMachineConnector(py_vmomi_service,
                                                                              resource_connection_details_retriever,
                                                                              dv_port_group_creator,
                                                                              virtual_machine_port_group_configurer)

        si = py_vmomi_service.connect(credentials.host, credentials.username,
                                      credentials.password,
                                      credentials.port)

        virtual_machine_path = 'Boris'
        virtual_machine_name = 'boris1'
        vm_uuid = self.get_vm_uuid(py_vmomi_service, si, virtual_machine_name)
        port_group_path = 'QualiSB'
        dv_switch_path = 'QualiSB'
        dv_switch_name = 'dvSwitch'
        dv_port_name = 'boris_group21'

        # Act
        virtual_switch_to_machine_connector.connect(virtual_machine_name, dv_switch_path, dv_switch_name,
                                                    dv_port_name, virtual_machine_path, vm_uuid,
                                                    port_group_path)

    def get_vm_uuid(self, py_vmomi_service, si, virtual_machine_name):
        vm = py_vmomi_service.get_obj(si.content, [vim.VirtualMachine], virtual_machine_name)
        vm_uuid = vm.config.uuid
        return vm_uuid