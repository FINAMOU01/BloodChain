const { ethers } = require("hardhat");

async function main() {
  const BloodUnit = await ethers.getContractFactory("BloodUnit");
  const bloodUnit = await BloodUnit.deploy();

  await bloodUnit.waitForDeployment();

  console.log("BloodUnit deployed to:", await bloodUnit.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
