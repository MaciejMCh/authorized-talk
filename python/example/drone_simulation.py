from asyncio import run
from typing import cast
from google.protobuf.message import Message
from python.blockchain.account import Account
from python.blockchain.identity_server_contract import IdentityServerContract
from python.example.actor import Actor
from python.example.drone_simulation_controller import DroneSimulationController
from python.example.proto.system_pb2 import ReadTelemetry, Drone, TakeOff, Success
from python.websocket.location import Location


class DroneSimulation:
    def __init__(
        self,
        account: Account,
        websocket_location: Location,
        identity_server_contract: IdentityServerContract,
    ):
        self.actor = Actor(
            actor_type=Drone,
            identity_server_contract=identity_server_contract,
            account=account,
            websocket_location=websocket_location,
            handle_command=self.receive_command,
        )
        self.drone_simulation_controller = DroneSimulationController()

    def receive_command(self, command: Message) -> Message:
        if isinstance(command, ReadTelemetry):
            request_telemetry_command = cast(ReadTelemetry, command)
        if isinstance(command, TakeOff):
            self.drone_simulation_controller.take_off()
            return TakeOff.Result(success=Success())

        raise Exception(f"unexpected command {command}")
