const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Rewards Contract", function () {
  let rewards;
  let owner;
  let recipient;
  let nonOwner;

  beforeEach(async function () {
    const Rewards = await ethers.getContractFactory("Rewards");
    rewards = await Rewards.deploy();
    await rewards.waitForDeployment();

    const signers = await ethers.getSigners();
    owner = signers[0];
    recipient = signers[1];
    nonOwner = signers[2];
  });

  it("should deploy successfully", async function () {
    const address = await rewards.getAddress();
    expect(address).to.not.equal(null);
  });

  it("should mint tokens to a recipient", async function () {
    await rewards.mintReward(recipient.address, 10, "bag-001");
    const balance = await rewards.getBalance(recipient.address);
    expect(balance).to.equal(10);
  });

  it("should emit TokensMinted event", async function () {
    const tx = await rewards.mintReward(recipient.address, 10, "bag-001");
    await expect(tx)
      .to.emit(rewards, "TokensMinted")
      .withArgs(recipient.address, 10, "bag-001");
  });

  it("should reject mint from non-owner", async function () {
    const rewardsAsNonOwner = rewards.connect(nonOwner);
    await expect(
      rewardsAsNonOwner.mintReward(recipient.address, 10, "bag-001")
    ).to.be.revertedWith("Not authorized");
  });
});
