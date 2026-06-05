const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Rewards Contract", function () {
  let rewards;
  let owner;
  let recipient;
  let recipient2;
  let nonOwner;

  beforeEach(async function () {
    const Rewards = await ethers.getContractFactory("Rewards");
    rewards = await Rewards.deploy();
    await rewards.waitForDeployment();

    const signers = await ethers.getSigners();
    owner = signers[0];
    recipient = signers[1];
    recipient2 = signers[2];
    nonOwner = signers[3];
  });

  it("should deploy successfully", async function () {
    const address = await rewards.getAddress();
    expect(address).to.not.equal(null);
  });

  it("should set deployer as owner", async function () {
    expect(await rewards.owner()).to.equal(owner.address);
  });

  it("should mint tokens to a recipient", async function () {
    await rewards.mintReward(recipient.address, 10, "bag-001");
    const balance = await rewards.getBalance(recipient.address);
    expect(balance).to.equal(10);
  });

  it("should accumulate tokens on multiple mints to same recipient", async function () {
    await rewards.mintReward(recipient.address, 10, "bag-001");
    await rewards.mintReward(recipient.address, 5, "bag-002");
    const balance = await rewards.getBalance(recipient.address);
    expect(balance).to.equal(15);
  });

  it("should mint to multiple recipients", async function () {
    await rewards.mintReward(recipient.address, 10, "bag-001");
    await rewards.mintReward(recipient2.address, 20, "bag-002");
    expect(await rewards.getBalance(recipient.address)).to.equal(10);
    expect(await rewards.getBalance(recipient2.address)).to.equal(20);
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

  it("should mint zero tokens", async function () {
    await rewards.mintReward(recipient.address, 0, "bag-zero");
    const balance = await rewards.getBalance(recipient.address);
    expect(balance).to.equal(0);
  });

  it("should accept empty string as bag ID", async function () {
    await rewards.mintReward(recipient.address, 5, "");
    const balance = await rewards.getBalance(recipient.address);
    expect(balance).to.equal(5);
  });

  it("should return zero for unregistered address", async function () {
    const balance = await rewards.getBalance(nonOwner.address);
    expect(balance).to.equal(0);
  });

  it("should track owner balance separately", async function () {
    await rewards.mintReward(recipient.address, 10, "bag-001");
    await rewards.mintReward(owner.address, 25, "bag-owner");
    expect(await rewards.getBalance(recipient.address)).to.equal(10);
    expect(await rewards.getBalance(owner.address)).to.equal(25);
  });
});
