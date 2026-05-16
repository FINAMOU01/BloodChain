// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

contract Rewards {
    address public owner;
    mapping(address => uint256) public balances;
    
    event TokensMinted(address indexed recipient, uint256 amount, string bagId);
    
    constructor() {
        owner = msg.sender;
    }
    
    function mintReward(address recipient, uint256 amount, string memory bagId) public {
        require(msg.sender == owner, "Not authorized");
        balances[recipient] += amount;
        emit TokensMinted(recipient, amount, bagId);
    }
    
    function getBalance(address account) public view returns (uint256) {
        return balances[account];
    }
}
