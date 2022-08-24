import time
import unittest
from typing import Optional
from python.example.proto.system_pb2 import TelemetryUpdateMessage
from python.example.tests.testSuite import TestConnector, TestMedium
from python.example.viewer import Viewer


class ViewerTestCase(unittest.TestCase):
    def testReceivingTelemetry(self):
        receivedTelemetry: Optional[TelemetryUpdateMessage] = None

        testConnector = TestConnector()

        def onTelemetryUpdate(telemetry: TelemetryUpdateMessage):
            nonlocal receivedTelemetry
            receivedTelemetry = telemetry

        viewer = Viewer(
            targetPseudonym='drone',
            onTelemetryUpdate=onTelemetryUpdate,
            connector=testConnector,
        )

        viewer.requestTelemetry()
        testConnector.testMedium.receive(TelemetryUpdateMessage(batteryLevel=0.9).SerializeToString())
        self.assertIsNotNone(receivedTelemetry)


if __name__ == '__main__':
    unittest.main()
