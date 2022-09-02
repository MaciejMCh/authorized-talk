pragma solidity ^0.8.0;

contract AlwaysCompiles {
    function echo(string memory message) public returns (string memory) {
        return message;
    }
}
