from python.core.interfaceIdentity import InterfaceIdentity
from python.example.proto.system_pb2 import TelemetryUpdateMessage
from python.example.viewer import Viewer, Connector


class TestConnector(Connector):
    pass


testConnector = TestConnector()


def onTelemetryUpdate(telemetry: TelemetryUpdateMessage):
    print('telemetry did update', telemetry)


viewer = Viewer(
    targetPseudonym='drone',
    onTelemetryUpdate=onTelemetryUpdate,
    connector=testConnector,
)

viewer.requestTelemetry()
