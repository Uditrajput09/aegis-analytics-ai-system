/** @type import('hardhat/config').HardhatUserConfig */
require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

const WALLET_PRIVATE_KEY     = process.env.WALLET_PRIVATE_KEY     || "0x0000000000000000000000000000000000000000000000000000000000000001";
const CHAIN_RPC_URL          = process.env.CHAIN_RPC_URL          || "";
const ETHERSCAN_API_KEY      = process.env.ETHERSCAN_API_KEY      || "";
const POLYGONSCAN_API_KEY    = process.env.POLYGONSCAN_API_KEY    || "";

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: { enabled: true, runs: 200 },
    },
  },

  networks: {
    // ── Local development ───────────────────────────────────────────────────
    localhost: {
      url: "http://127.0.0.1:8545",
    },

    // ── Sepolia Testnet ─────────────────────────────────────────────────────
    sepolia: {
      url: CHAIN_RPC_URL || `https://sepolia.infura.io/v3/${process.env.INFURA_PROJECT_ID || ""}`,
      chainId: 11155111,
      accounts: [WALLET_PRIVATE_KEY],
    },

    // ── Polygon Mainnet ─────────────────────────────────────────────────────
    polygon: {
      url: "https://polygon-rpc.com",
      chainId: 137,
      accounts: [WALLET_PRIVATE_KEY],
      gasPrice: 30_000_000_000,  // 30 gwei
    },

    // ── Polygon Amoy Testnet ────────────────────────────────────────────────
    polygonAmoy: {
      url: "https://rpc-amoy.polygon.technology",
      chainId: 80002,
      accounts: [WALLET_PRIVATE_KEY],
    },
  },

  etherscan: {
    apiKey: {
      sepolia:     ETHERSCAN_API_KEY,
      polygon:     POLYGONSCAN_API_KEY,
      polygonAmoy: POLYGONSCAN_API_KEY,
    },
    customChains: [
      {
        network: "polygonAmoy",
        chainId: 80002,
        urls: {
          apiURL:    "https://api-amoy.polygonscan.com/api",
          browserURL:"https://amoy.polygonscan.com",
        },
      },
    ],
  },

  paths: {
    sources:   "./contracts",
    tests:     "./contracts/test",
    cache:     "./contracts/.cache",
    artifacts: "./contracts/artifacts",
  },
};
