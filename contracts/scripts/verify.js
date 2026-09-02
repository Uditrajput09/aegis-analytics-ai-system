const hre = require("hardhat");

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log("Usage: npx hardhat run scripts/verify.js --network sepolia <PriceAnchorAddr> <PredictionAuditAddr>");
    return;
  }

  const [priceAnchorAddr, predictionAuditAddr] = args;

  console.log(`Verifying PriceAnchor at ${priceAnchorAddr}...`);
  await hre.run("verify:verify", {
    address: priceAnchorAddr,
    constructorArguments: [],
  });

  console.log(`Verifying PredictionAudit at ${predictionAuditAddr}...`);
  await hre.run("verify:verify", {
    address: predictionAuditAddr,
    constructorArguments: [],
  });

  console.log("Contract verification complete.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
