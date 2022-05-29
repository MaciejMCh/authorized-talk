pragma solidity >=0.7.0 <0.9.0;

contract AuthorizedTalk {
    struct SslConnection {
        string url;
    }

    struct Interface {
        string name;
        string[] whitelist;
    }

    struct Talker {
        address walletAddress;
        string pseudonym;
        SslConnection sslConnection;
        string publicKey;
    }

    mapping (string => Talker) talkersByPseudonyms;

    mapping (address => Talker) talkersByAddresses;

    mapping (string => Interface) interfacesByIdentities;

    constructor() public {}

    function echo(string memory message) public returns (string memory) {
        return message;
    }

    function requestConnection(string memory targetPseudonym, string memory interfaceName) public returns (string memory) {
        Talker memory talker = talkersByPseudonyms[targetPseudonym];
        return talker.sslConnection.url;
    }

    function getPublicKey(string memory targetPseudonym) public returns (string memory) {
        Talker memory talker = talkersByPseudonyms[targetPseudonym];
        return talker.publicKey;
    }

    function registerTalker(string memory pseudonym, SslConnection calldata sslConnection, string memory publicKey) public {
        Talker memory talker = Talker({
            walletAddress: msg.sender,
            pseudonym: pseudonym,
            sslConnection: sslConnection,
            publicKey: publicKey
        });
        talkersByPseudonyms[talker.pseudonym] = talker;
        talkersByAddresses[talker.walletAddress] = talker;
    }

    function canAccess(string memory sourcePseudonym, string memory targetInterface) public returns (bool) {
        Talker memory meTalker = talkersByAddresses[msg.sender];
        string memory interfaceId = this.interfaceIdentity(meTalker.pseudonym, targetInterface);
        Interface memory interf = interfacesByIdentities[interfaceId];
        return true;
    }

    function interfaceIdentity(string memory pseudonym, string memory targetInterface) public returns (string memory) {
        return string(abi.encodePacked(pseudonym, targetInterface));
    }
}
