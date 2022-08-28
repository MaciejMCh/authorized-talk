from typing import List, Callable
from python.core.interface_identity import InterfaceIdentity
from python.medium.connector import Connector
from python.medium.medium import Medium
from python.medium.websocket_medium import WebsocketConnector
from python.medium.kinds import SourceMedium, TargetMedium, WebsocketTargetMedium


class FailedToResolveMedium(Exception):
    pass


async def resolve_medium(source: SourceMedium, target: TargetMedium) -> Medium:
    if isinstance(target, WebsocketTargetMedium):
        return await WebsocketConnector.establish_connection(target.location)
    raise FailedToResolveMedium()


class CompromiseConnector(Connector):
    def __init__(self, sources: List[SourceMedium], targets: List[TargetMedium]):
        self.sources = sources
        self.targets = targets

    async def establish_connection(
            self,
            interface_identity: InterfaceIdentity,
            on_message: Callable[[bytes], None],
    ) -> Medium:
        for target in self.targets:
            for source in self.sources:
                if target.kind == source.kind:
                    return await resolve_medium(
                        source=source,
                        target=target,
                    )
        raise FailedToResolveMedium()
