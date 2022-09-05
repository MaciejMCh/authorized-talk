from typing import cast
from google.protobuf.message import Message
from python.blockchain.account import Account
from python.blockchain.identity_server_contract import IdentityServerContract
from python.core.random import BuiltInRandom
from python.core.rsa_keys import RsaKeys
from python.example.drone_simulation_controller import DroneSimulationController
from python.example.implement_actor import implement_actor
from python.example.proto.system_pb2 import Drone, RequestTelemetryCommand, TakeOffCommand
from python.identity_server.blockchain_identity_server import BlockchainIdentityServer
from python.medium.authorized.server import AuthorizedServerMedium
from python.medium.websocket_medium import WebsocketMedium
from python.websocket.location import Location
from python.websocket.server import run_server, WebsocketServerSession


class DroneSimulation:
    def __init__(
        self,
        identity_server_contract: IdentityServerContract,
        account: Account,
        websocket_location: Location,
    ):
        self.identity_server_contract = identity_server_contract
        self.identity_server = BlockchainIdentityServer(identity_server_contract)
        self.account = account
        self.websocket_location = websocket_location
        self.rsa_keys = RsaKeys.generate()
        self.drone_simulation_controller = DroneSimulationController()
        self.initialize()

    def initialize(self):
        self.connect_to_identity_server()
        self.open_websocket()

    def open_websocket(self):
        server, server_close = await run_server(self.websocket_location)

        def on_session_opened(session: WebsocketServerSession):
            medium = AuthorizedServerMedium(
                pseudonym=self.account.pseudonym,
                medium=WebsocketMedium.server(session),
                rsa_keys=self.rsa_keys,
                identity_server=self.identity_server,
                random=BuiltInRandom(),
            )
            interface = await medium.authorized
            implement_interface()

        server.handle_session_opened(on_session_opened)

    def connect_to_identity_server(self):
        self.identity_server_contract.connect(
            account=self.account,
            publicKey=self.rsa_keys.public_key,
            websocketLocation=self.websocket_location,
        )

    def receive_command(self, command: Message):
        if isinstance(command, RequestTelemetryCommand):
            request_telemetry_command = cast(RequestTelemetryCommand, command)
            return
        if isinstance(command, TakeOffCommand):
            take_off_command = cast(TakeOffCommand, command)
            return

        raise Exception(f"unexpected command {command}")
