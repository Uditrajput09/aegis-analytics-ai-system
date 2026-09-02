/**
 * deploy.js — Hardhat deployment script for Aegis Analytics AI smart contracts.
 *
 * Usage:
 *   npx hardhat run contracts/scripts/deploy.js --network sepolia
 *   npx hardhat run contracts/scripts/deploy.js --network polygon
 *
 * After deployment, copy the contract addresses into your .env file:
 *   PRICE_ANCHOR_CONTRACT=0x...
 *   PREDICTION_AUDIT_CONTRACT=0x...
 */

const hre = require("hardhat");

async function main() {
    const [deployer] = await hre.ethers.getSigners();

    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    console.log("  Aegis Analytics AI — Smart Contract Deployment");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    console.log(`  Network:  ${hre.network.name} (chainId: ${hre.network.config.chainId})`);
    console.log(`  Deployer: ${deployer.address}`);

    const balance = await hre.ethers.provider.getBalance(deployer.address);
    console.log(`  Balance:  ${hre.ethers.formatEther(balance)} ETH/MATIC`);
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n");

    // ── Deploy PriceAnchor ────────────────────────────────────────────────────
    console.log("Deploying PriceAnchor...");
    const PriceAnchor = await hre.ethers.getContractFactory("PriceAnchor");
    const priceAnchor = await PriceAnchor.deploy();
    await priceAnchor.waitForDeployment();
    const priceAnchorAddr = await priceAnchor.getAddress();
    console.log(`✅ PriceAnchor deployed at: ${priceAnchorAddr}\n`);

    // ── Deploy PredictionAudit ────────────────────────────────────────────────
    console.log("Deploying PredictionAudit...");
    const PredictionAudit = await hre.ethers.getContractFactory("PredictionAudit");
    const predictionAudit = await PredictionAudit.deploy();
    await predictionAudit.waitForDeployment();
    const predictionAuditAddr = await predictionAudit.getAddress();
    console.log(`✅ PredictionAudit deployed at: ${predictionAuditAddr}\n`);

    // ── Summary ───────────────────────────────────────────────────────────────
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    console.log("  ✅ Deployment complete! Add these to your .env file:");
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    console.log(`  PRICE_ANCHOR_CONTRACT=${priceAnchorAddr}`);
    console.log(`  PREDICTION_AUDIT_CONTRACT=${predictionAuditAddr}`);
    console.log(`  BLOCKCHAIN_ENABLED=true`);
    console.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");

    // Optionally verify on Etherscan / Polygonscan
    if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
        console.log("\nWaiting 5 blocks for Etherscan indexing...");
        await priceAnchor.deploymentTransaction().wait(5);

        try {
            await hre.run("verify:verify", { address: priceAnchorAddr });
            await hre.run("verify:verify", { address: predictionAuditAddr });
            console.log("✅ Contracts verified on block explorer.");
        } catch (err) {
            console.warn("⚠️  Verification failed (may need ETHERSCAN_API_KEY):", err.message);
        }
    }
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});
