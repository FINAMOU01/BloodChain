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
});
