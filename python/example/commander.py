from asyncio import get_running_loop, Future
from typing import Dict

from python.blockchain.account import Account
from python.blockchain.identity_server_contract import IdentityServerContract
from python.core.interface_identity import InterfaceIdentity
from python.core.random import BuiltInRandom
from python.core.rsa_keys import RsaKeys
from python.example.compose_command import compose_command
from python.example.proto.system_pb2 import Message
from python.identity_server.blockchain_identity_server import BlockchainIdentityServer
from python.identity_server.identity_server import IdentityServer
from python.medium.authorized.client import AuthorizedClientMedium
from python.medium.kinds import WebsocketSourceMedium


class Commander:
    def __init__(
        self,
        account: Account,
        target: InterfaceIdentity,
        identity_server_contract: IdentityServerContract,
    ):
        self.nonce = 0
        self.pending_commands: Dict[int, Future[Message]] = {}
        self.medium = AuthorizedClientMedium(
            pseudonym=account.pseudonym,
            target=target,
            identity_server=BlockchainIdentityServer(identity_server_contract),
            available_source_mediums=[WebsocketSourceMedium()],
            rsa_keys=RsaKeys.generate(),
            random=BuiltInRandom(),
        )

    def send(self, message: Message) -> Message:
        self.nonce += 1
        command = compose_command(message=message, nonce=self.nonce)
        future: Future[Message] = get_running_loop().create_future()
        self.pending_commands[self.nonce] = future
        command_bytes = command.SerializeToString()
        self.medium.send(command_bytes)
