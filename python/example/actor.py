from asyncio import create_task
from typing import cast, Callable
from google.protobuf.message import Message
from google.protobuf.reflection import GeneratedProtocolMessageType
from python.blockchain.account import Account
from python.blockchain.identity_server_contract import IdentityServerContract
from python.core.random import BuiltInRandom
from python.core.rsa_keys import RsaKeys
from python.example.drone_simulation_controller import DroneSimulationController
from python.example.implement_interface import implement_interface
from python.identity_server.blockchain_identity_server import BlockchainIdentityServer
from python.medium.authorized.server import AuthorizedServerMedium
from python.medium.websocket_medium import WebsocketMedium
from python.websocket.location import Location
from python.websocket.server import run_server, WebsocketServerSession


DEBUG = True


class Actor:
    def __init__(
        self,
        actor_type: GeneratedProtocolMessageType,
        identity_server_contract: IdentityServerContract,
        account: Account,
        websocket_location: Location,
        handle_command: Callable[[Message], Message],
    ):
        self.actor_type = actor_type
        self.identity_server_contract = identity_server_contract
        self.identity_server = BlockchainIdentityServer(identity_server_contract)
        self.account = account
        self.websocket_location = websocket_location
        self.handle_command = handle_command
        self.rsa_keys = RsaKeys.generate()
        self.drone_simulation_controller = DroneSimulationController()
        self.initialize()

    def initialize(self):
        self.connect_to_identity_server()
        create_task(self.open_websocket())

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
                    actor_type=self.actor_type,
                    interface=interface,
                    medium=medium,
                    handle_command=self.handle_command,
                )
            create_task(do())

        server.handle_session_opened(on_session_opened)

    def connect_to_identity_server(self):
        debug_print(f"connect to identity server:\n\taccount:\t\t{self.account.pseudonym}\n\tpublic key:\t\t{self.rsa_keys.public_key}")
        self.identity_server_contract.connect(
            account=self.account,
            publicKey=self.rsa_keys.public_key,
            websocketLocation=self.websocket_location,
        )


def debug_print(message: str):
    if DEBUG:
        print(f"actor: {message}")
