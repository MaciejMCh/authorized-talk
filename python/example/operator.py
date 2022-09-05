from python.blockchain.account import Account
from python.blockchain.identity_server_contract import IdentityServerContract
from python.core.interface_identity import InterfaceIdentity
from python.example.actor import Actor
from python.example.commander import Commander
from python.example.proto.system_pb2 import TakeOff
from python.identity_server.identity_server import IdentityServer


class Operator:
    def __init__(
        self,
        account: Account,
        target: InterfaceIdentity,
        identity_server: IdentityServer,
    ):
        self.commander = Commander(
            account=account,
            target=target,
            identity_server=identity_server,
        )

    async def verify_drone(self) -> bool:
        take_off_result: TakeOff.Result = self.commander.send(TakeOff())
        return take_off_result.WhichOneOf("result") == "success"
