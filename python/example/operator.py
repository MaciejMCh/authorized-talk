from python.blockchain.account import Account
from python.blockchain.identity_server_contract import IdentityServerContract
from python.core.interface_identity import InterfaceIdentity
from python.example.commander import Commander
from python.example.proto.system_pb2 import TakeOff, Drone


class Operator:
    def __init__(
        self,
        account: Account,
        target: InterfaceIdentity,
        identity_server_contract: IdentityServerContract,
    ):
        self.commander = Commander(
            account=account,
            target=target,
            target_actor_type=Drone,
            identity_server_contract=identity_server_contract,
        )

    async def verify_drone(self) -> bool:
        take_off_result: TakeOff.Result = await self.commander.send(TakeOff())
        return take_off_result.WhichOneOf("result") == "success"
