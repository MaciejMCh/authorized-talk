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

    mapping(address => string[]) private roles;

    mapping(address => mapping(string => string[])) private whitelist;

    function connect(bytes calldata publicKey, WebsocketMedium calldata websocketMedium) external {
        Actor memory newActor = Actor({
            publicKey: publicKey,
            websocketMedium: websocketMedium,
            registered: true
        });

        actors[msg.sender] = newActor;
    }

    function assignRoles(address actor, string[] calldata rolesToAssign) external {
        for (uint i=0; i<rolesToAssign.length; i++) {
            roles[actor].push(rolesToAssign[i]);
        }
    }

    function addToWhitelist(
        address actor,
        string calldata accessInterface,
        string[] calldata accessRoles
    ) external {
        for (uint i=0; i<accessRoles.length; i++) {
            whitelist[actor][accessInterface].push(accessRoles[i]);
        }
    }

    function getActor(address identity) external view returns (Actor memory) {
        return actors[identity];
    }

    function hasAccess(
        address sourceActor,
        address targetActor,
        string calldata targetInterface
    ) external view returns (bool) {
        string[] memory permittedRoles = whitelist[targetActor][targetInterface];
        string[] memory sourceRoles = roles[sourceActor];

        for (uint permittedRoleIndex=0; permittedRoleIndex<permittedRoles.length; permittedRoleIndex++) {
            for (uint sourceRoleIndex=0; sourceRoleIndex<sourceRoles.length; sourceRoleIndex++) {
                if (compareStrings(permittedRoles[permittedRoleIndex], sourceRoles[sourceRoleIndex])) {
                    return true;
                }
            }
        }

        return false;
    }

    function compareStrings(string memory a, string memory b) internal pure returns (bool) {
        return keccak256(abi.encodePacked(a)) == keccak256(abi.encodePacked(b));
    }
}
