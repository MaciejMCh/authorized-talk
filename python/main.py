import asyncio
from asyncio import gather, sleep
from typing import Optional

from python.blockchain.blockchain import Blockchain
from python.blockchain.identity_server_contract import IdentityServerContract
from python.core.interface_identity import InterfaceIdentity
from python.core.rsa_keys import RsaKeys
from python.encryption.rsa_encryption import RsaEncryption
from python.example.drone_simulation import DroneSimulation
from python.example.operator import Operator
from python.medium.authorized.client import AuthorizedClientMedium
from python.medium.authorized.server import AuthorizedServerMedium
from python.medium.authorized.utils import introduction_signature
from python.medium.kinds import WebsocketTargetMedium, WebsocketSourceMedium
from python.medium.medium import Medium
from python.medium.websocket_medium import WebsocketConnector, WebsocketMedium
from python.messages.whisper_control_pb2 import Introduction, Challenge, ChallengeAnswer, AccessPass
from python.tests.authorized_medium.utils import with_introducing_status, with_submitting_status, with_initial_status, \
    with_challenged_status
from python.tests.smart_contract.test_accounts import test_accounts
from python.tests.utils import TestIdentityServer, bob_public_key, alice_rsa_keys, bob_private_key, TestRandom
from python.websocket.location import Location
from python.websocket.server import run_server
from python.websocket.client import run_client


def assertTrue(condition: bool):
    print('assertTrue', condition)


async def main():
    blockchain = Blockchain.local()
    accounts = test_accounts(blockchain)
    identity_server_contract = IdentityServerContract.deploy(
        blockchain=blockchain,
        account=accounts.admin,
    )

    drone_simulation = DroneSimulation(
        account=accounts.bob,
        websocket_location=Location(host="localhost", port=9876),
        identity_server_contract=identity_server_contract,
    )

    operator = Operator(
        account=accounts.alice,
        target=InterfaceIdentity(
            pseudonym=accounts.bob.pseudonym,
            interface="controller",
        ),
        identity_server_contract=identity_server_contract,
    )

    await sleep(1)

    await operator.verify_drone()

    # self.assertIsInstance(drone_simulation.drone_simulation_controller.command, TakeOff, "command should be take of")

if __name__ == "__main__":
    asyncio.run(main())
