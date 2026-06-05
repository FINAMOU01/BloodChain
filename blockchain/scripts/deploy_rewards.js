const hre = require("hardhat");

async function main() {
  const RewardsFactory = await hre.ethers.getContractFactory("Rewards");
  const rewards = await RewardsFactory.deploy();
  await rewards.waitForDeployment();
  console.log("Rewards contract deployed to", await rewards.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
