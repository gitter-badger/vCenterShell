import os
import sys
from unittest import TestCase
from pycommon.logging_service import LoggingService
import xml.etree.ElementTree as ET

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../vCenterShell'))


class TestDataModel(TestCase):
    LoggingService("CRITICAL", "DEBUG", None)

    def test_resource_models(self):
        ns = {'default': 'http://schemas.qualisystems.com/ResourceManagement/ExportImportConfigurationSchema.xsd'}
        datamodel_path = os.path.join(os.path.dirname(__file__), '../vCenterShellPackage/DataModel/datamodel.xml')
        tree = ET.parse(datamodel_path)
        root = tree.getroot()
        resource_models = root.findall('.//default:ResourceModel', ns)
        validation_errors = []
        for resource_model in resource_models:
            model_name = resource_model.attrib['Name'].replace(' ', '') + 'ResourceModel'

            try:
                klass = self.get_class('models.' + model_name)
            except ValueError as value_error:
                validation_errors.append(value_error.message)
                continue

            # foreach model_attribute in resource_model
            # hasattr(getattr(getattr(imported_model,'VirtualNicModel'),'VirtualNicModel')('','','',''),'macAddress')

            # imported_model = __import__('models', fromlist=['VirtualNicModel'])

        for validation_error in validation_errors:
            print validation_error

        self.assertSequenceEqual(validation_errors, [])

    def get_class(self, class_path):
        module_path, class_name = class_path.rsplit(".", 1)

        try:
            module = __import__(module_path, fromlist=[class_name])
        except ImportError:
            raise ValueError("Module '%s' could not be imported" % (module_path,))

        try:
            cls = getattr(module, class_name)
        except AttributeError:
            raise ValueError("Module '%s' has no class '%s'" % (module_path, class_name,))

        return cls