from asyncio import get_running_loop, Future
from typing import Dict, Optional, Tuple
from google.protobuf.message import Message
from python.blockchain.account import Account
from python.blockchain.identity_server_contract import IdentityServerContract
from python.core.interface_identity import InterfaceIdentity
from google.protobuf.reflection import GeneratedProtocolMessageType
from python.core.random import BuiltInRandom
from python.core.rsa_keys import RsaKeys
from python.example.blank_result import blank_result
from python.example.compose_command import compose_command
from python.example.proto.system_pb2 import Result
from python.identity_server.blockchain_identity_server import BlockchainIdentityServer
from python.medium.authorized.client import AuthorizedClientMedium
from python.medium.kinds import WebsocketSourceMedium
from python.websocket.location import Location


class Commander:
    def __init__(
        self,
        account: Account,
        target_actor_type: GeneratedProtocolMessageType,
        target: InterfaceIdentity,
        identity_server_contract: IdentityServerContract,
    ):
        self.account = account
        self.target_actor_type = target_actor_type
        self.target = target
        self.identity_server_contract = identity_server_contract
        self.rsa_keys = RsaKeys.generate()
        self.nonce = 0
        self.pending_commands: Dict[int, Tuple[Future[Message], Message]] = {}
        self.medium: Optional[AuthorizedClientMedium] = None
        self.initialize()

    def initialize(self):
        self.connect_to_identity_server()
        self.connect_to_target()

    def connect_to_target(self):
        self.medium = AuthorizedClientMedium(
            pseudonym=self.account.pseudonym,
            target=self.target,
            identity_server=BlockchainIdentityServer(self.identity_server_contract),
            available_source_mediums=[WebsocketSourceMedium()],
            rsa_keys=self.rsa_keys,
            random=BuiltInRandom(),
        )
        self.medium.handle_message(self.on_message)

    def connect_to_identity_server(self):
        self.identity_server_contract.connect(
            account=self.account,
            publicKey=self.rsa_keys.public_key,
            websocketLocation=Location(host="", port=0),
        )

    async def send(self, message: Message) -> Message:
        self.nonce += 1
        command = compose_command(actor_type=self.target_actor_type, message=message, nonce=self.nonce)
        future: Future[Message] = get_running_loop().create_future()
        self.pending_commands[self.nonce] = (future, blank_result(message))
        command_bytes = command.SerializeToString()
        await self.medium.send(command_bytes)
        return await future

    def on_message(self, message: bytes):
        wrapper_result = Result()
        wrapper_result.ParseFromString(message)
        future, command_result = self.pending_commands[wrapper_result.requestNonce]
        command_result.ParseFromString(wrapper_result.result)
        future.set_result(command_result)
