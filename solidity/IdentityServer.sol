// SPDX-License-Identifier: MIT

pragma solidity 0.8.7;

error IdentityServer__ActorAlreadyExists();

contract IdentityServer {
    struct WebsocketMedium {
        string host;
        uint16 port;
    }

    struct Actor {
        bytes publicKey;
        WebsocketMedium websocketMedium;
        bool registered;
    }

    mapping(address => Actor) private actors;

    function connect(bytes calldata publicKey, WebsocketMedium calldata websocketMedium) external {
        Actor memory newActor = Actor({
            publicKey: publicKey,
            websocketMedium: websocketMedium,
            registered: true
        });

        actors[msg.sender] = newActor;
    }

    function getActor(address identity) external view returns (Actor memory) {
        return actors[identity];
    }
}
