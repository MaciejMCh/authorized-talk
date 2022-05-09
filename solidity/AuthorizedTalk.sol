pragma solidity >0.5.0;

contract Greeter {
    string public greeting;

    constructor() public {
        greeting = 'Hello';
    }

    function setGreeting(string memory _greeting) public returns (string memory) {
        greeting = _greeting;
        return greeting;
    }

    function echo(string memory _message) public returns (string memory) {
        return _message;
    }

    function greet() view public returns (string memory) {
        return greeting;
    }
}
