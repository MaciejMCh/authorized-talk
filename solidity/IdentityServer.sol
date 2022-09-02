// SPDX-License-Identifier: MIT

pragma solidity 0.8.7;

error IdentityServer__ActorAlreadyExists();

contract IdentityServer {
    struct WebsocketMedium {
        string host;
        uint16 port;
    }

    struct Actor {
        string pseudonym;
        bytes publicKey;
        WebsocketMedium websocketMedium;
        bool registered;
    }

    mapping(address => Actor) private actors;

    function connect(
        string calldata pseudonym,
        bytes calldata publicKey,
        WebsocketMedium calldata websocketMedium
    )
        external
    {
        Actor memory existingActor = actors[msg.sender];
        if (existingActor.registered && !compareStrings(pseudonym, existingActor.pseudonym)) {
            revert IdentityServer__ActorAlreadyExists();
        }

        Actor memory newActor = Actor({
            pseudonym: pseudonym,
            publicKey: publicKey,
            websocketMedium: websocketMedium,
            registered: true
        });

        actors[msg.sender] = newActor;
    }

    function compareStrings(
        string memory a,
        string memory b
    )
        internal
        pure
        returns (bool)
    {
        return keccak256(abi.encodePacked(a)) == keccak256(abi.encodePacked(b));
    }

    function myPseudonym()
        external
        view
        returns (string memory)
    {
        Actor memory me = actors[msg.sender];
        return me.pseudonym;
    }
}
