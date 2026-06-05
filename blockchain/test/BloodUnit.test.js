const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("BloodUnit Contract", function () {
  let bloodUnit;

  beforeEach(async function () {
    const BloodUnit = await ethers.getContractFactory("BloodUnit");
    bloodUnit = await BloodUnit.deploy();
    await bloodUnit.waitForDeployment();
  });

  it("should deploy successfully", async function () {
    const address = await bloodUnit.getAddress();
    expect(address).to.not.be.null;
  });

  it("should register a blood bag", async function () {
    await bloodUnit.registerBag("test-bag-001", "O+");
    const bag = await bloodUnit.getBag("test-bag-001");
    expect(bag.bagId).to.equal("test-bag-001");
    expect(bag.bloodType).to.equal("O+");
    expect(bag.status).to.equal("collected");
  });

  it("should emit BagRegistered event", async function () {
    const tx = await bloodUnit.registerBag("test-bag-001", "O+");
    const receipt = await tx.wait();
    
    const event = receipt.logs
      .map(log => {
        try {
          return bloodUnit.interface.parseLog(log);
        } catch (e) {
          return null;
        }
      })
      .find(e => e && e.name === "BagRegistered");
    
    expect(event).to.not.be.null;
    expect(event.args[0]).to.equal("test-bag-001");
    expect(event.args[1]).to.equal("O+");
  });

  it("should accept all valid blood types", async function () {
    const types = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"];
    for (const bt of types) {
      await bloodUnit.registerBag(`bag-${bt}`, bt);
      const bag = await bloodUnit.getBag(`bag-${bt}`);
      expect(bag.bloodType).to.equal(bt);
    }
  });

  it("should overwrite existing bag on duplicate ID", async function () {
    await bloodUnit.registerBag("bag-001", "O+");
    await bloodUnit.registerBag("bag-001", "A-");
    const bag = await bloodUnit.getBag("bag-001");
    expect(bag.bloodType).to.equal("A-");
  });

  it("should return empty bag for unregistered ID", async function () {
    const bag = await bloodUnit.getBag("nonexistent");
    expect(bag.bagId).to.equal("");
  });

  it("should accept empty string as bag ID", async function () {
    await bloodUnit.registerBag("", "O+");
    const bag = await bloodUnit.getBag("");
    expect(bag.bloodType).to.equal("O+");
  });

  it("should set status to collected on registration", async function () {
    await bloodUnit.registerBag("bag-status-test", "B+");
    const bag = await bloodUnit.getBag("bag-status-test");
    expect(bag.status).to.equal("collected");
  });

  it("should set a non-zero timestamp", async function () {
    await bloodUnit.registerBag("bag-ts-test", "A+");
    const bag = await bloodUnit.getBag("bag-ts-test");
    expect(bag.timestamp).to.be.greaterThan(0);
  });

  it("should allow anyone to register a bag", async function () {
    const [, other] = await ethers.getSigners();
    await bloodUnit.connect(other).registerBag("other-bag", "AB+");
    const bag = await bloodUnit.getBag("other-bag");
    expect(bag.bagId).to.equal("other-bag");
  });

  it("should register multiple bags", async function () {
    await bloodUnit.registerBag("bag-1", "A+");
    await bloodUnit.registerBag("bag-2", "B+");
    await bloodUnit.registerBag("bag-3", "O-");
    const bag1 = await bloodUnit.getBag("bag-1");
    const bag2 = await bloodUnit.getBag("bag-2");
    const bag3 = await bloodUnit.getBag("bag-3");
    expect(bag1.bloodType).to.equal("A+");
    expect(bag2.bloodType).to.equal("B+");
    expect(bag3.bloodType).to.equal("O-");
  });
});
