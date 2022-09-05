from asyncio import run
from typing import cast
from google.protobuf.message import Message
from python.blockchain.account import Account
from python.blockchain.identity_server_contract import IdentityServerContract
from python.core.random import BuiltInRandom
from python.core.rsa_keys import RsaKeys
from python.example.drone_simulation_controller import DroneSimulationController, TakeOff
from python.example.implement_interface import implement_interface
from python.example.proto.system_pb2 import ReadTelemetry, Drone
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
        run(self.open_websocket())

    async def open_websocket(self):
        server, server_close = await run_server(self.websocket_location)

        def on_session_opened(session: WebsocketServerSession):
            async def do():
                medium = AuthorizedServerMedium(
                    pseudonym=self.account.pseudonym,
                    medium=WebsocketMedium.server(session),
                    rsa_keys=self.rsa_keys,
                    identity_server=self.identity_server,
                    random=BuiltInRandom(),
                )
                interface = await medium.authorized
                implement_interface(
                    actor_type=Drone,
                    interface=interface,
                    medium=medium,
                    handle_command=self.receive_command,
                )
            run(do())

        server.handle_session_opened(on_session_opened)

    def connect_to_identity_server(self):
        self.identity_server_contract.connect(
            account=self.account,
            publicKey=self.rsa_keys.public_key,
            websocketLocation=self.websocket_location,
        )

    def receive_command(self, command: Message) -> Message:
        if isinstance(command, ReadTelemetry):
            request_telemetry_command = cast(ReadTelemetry, command)
            return
        if isinstance(command, TakeOff):
            take_off_command = cast(TakeOff, command)
            return

        raise Exception(f"unexpected command {command}")
