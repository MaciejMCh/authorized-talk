pragma solidity >=0.7.0 <0.9.0;

contract AuthorizedTalk {
    struct SslConnection {
        string url;
    }

    struct Talker {
        address walletAddress;
        string pseudonym;
        SslConnection sslConnection;
        string publicKey;
    }

    mapping (string => Talker) talkersByPseudonyms;

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
        talkersByPseudonyms[pseudonym] = Talker({
            walletAddress: msg.sender,
            pseudonym: pseudonym,
            sslConnection: sslConnection,
            publicKey: publicKey
        });
    }
}