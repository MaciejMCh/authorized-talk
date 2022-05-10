pragma solidity >=0.7.0 <0.9.0;

contract AuthorizedTalk {
    struct SslConnection {
        string url;
    }

    struct Talker {
        address walletAddress;
        string pseudonym;
        SslConnection sslConnection;
    }

    mapping (string => Talker) talkersByPseudonyms;

    mapping (int => string) qqq;

    string aaaa;

    uint256 number;

    constructor() public {}

    function echo(string memory message) public returns (string memory) {
        return message;
    }

    function requestConnection(string memory targetPseudonym, string memory interfaceName) public returns (string memory) {
        Talker memory talker = talkersByPseudonyms[targetPseudonym];
        return talker.sslConnection.url;
    }

    function registerTalker(string memory pseudonym, SslConnection calldata sslConnection) public {
        talkersByPseudonyms[pseudonym] = Talker({
            walletAddress: msg.sender,
            pseudonym: pseudonym,
            sslConnection: sslConnection
        });
    }

    function debug(uint256 num) public {
        number = num;
    }

    function debug2() public view returns (uint256) {
        return number;
    }
}