// SPDX-License-Identifier: MIT
pragma solidity 0.8.20;

contract BloodUnit {
    struct Bag {
        string bagId;
        string bloodType;
        string status;
        uint256 timestamp;
    }

    mapping(string => Bag) public bags;

    event BagRegistered(
        string bagId,
        string bloodType,
        string status,
        uint256 timestamp
    );

    function registerBag(string memory bagId, string memory bloodType) public {
        bags[bagId] = Bag({
            bagId: bagId,
            bloodType: bloodType,
            status: "collected",
            timestamp: block.timestamp
        });

        emit BagRegistered(bagId, bloodType, "collected", block.timestamp);
    }

    function getBag(string memory bagId) public view returns (Bag memory) {
        return bags[bagId];
    }
}
