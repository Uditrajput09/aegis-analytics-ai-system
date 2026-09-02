// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title PriceAnchor
 * @notice Stores immutable keccak256 hashes of OHLCV price bars on-chain.
 *
 * Deployed on: Sepolia testnet (development) / Polygon mainnet (production)
 *
 * Purpose:
 *   Allows anyone to verify that a price bar used in an Aegis Analytics AI
 *   prediction matches the hash stored on-chain at the time of ingestion.
 *   This provides a tamper-proof audit trail of raw market data.
 *
 * Key derivation (off-chain, in anchor_service.py):
 *   key = keccak256(abi.encodePacked(symbol, ":", timeframe, ":", ts_utc_iso))
 *
 * Hash derivation (off-chain, in anchor_service.py):
 *   dataHash = keccak256(JSON.stringify({symbol, timeframe, ts_utc, open, high, low, close, volume}))
 */
contract PriceAnchor {
    // ── Storage ───────────────────────────────────────────────────────────────

    struct PriceRecord {
        bytes32  dataHash;    // keccak256 of the canonical price JSON
        uint256  anchoredAt;  // block.timestamp when anchored
        address  submitter;   // wallet that submitted this anchor
    }

    /// @notice Map from price key → anchored record
    mapping(bytes32 => PriceRecord) public records;

    /// @notice Authorized submitters (only they can write records)
    mapping(address => bool) public authorizedSubmitters;

    address public owner;

    // ── Events ────────────────────────────────────────────────────────────────

    event PriceAnchored(
        bytes32 indexed key,
        bytes32 indexed dataHash,
        uint256 anchoredAt,
        address submitter
    );

    event SubmitterUpdated(address indexed submitter, bool authorized);

    // ── Modifiers ─────────────────────────────────────────────────────────────

    modifier onlyOwner() {
        require(msg.sender == owner, "PriceAnchor: not owner");
        _;
    }

    modifier onlyAuthorized() {
        require(
            authorizedSubmitters[msg.sender] || msg.sender == owner,
            "PriceAnchor: not authorized"
        );
        _;
    }

    // ── Constructor ───────────────────────────────────────────────────────────

    constructor() {
        owner = msg.sender;
        authorizedSubmitters[msg.sender] = true;
    }

    // ── Write Functions ───────────────────────────────────────────────────────

    /**
     * @notice Anchor a price bar hash on-chain.
     * @param key      keccak256 identifier for this (symbol, timeframe, ts_utc) tuple.
     * @param dataHash keccak256 hash of the canonical price bar JSON payload.
     */
    function anchorPrice(bytes32 key, bytes32 dataHash) external onlyAuthorized {
        records[key] = PriceRecord({
            dataHash:   dataHash,
            anchoredAt: block.timestamp,
            submitter:  msg.sender
        });

        emit PriceAnchored(key, dataHash, block.timestamp, msg.sender);
    }

    /**
     * @notice Authorize or revoke a submitter wallet.
     */
    function setSubmitter(address submitter, bool authorized) external onlyOwner {
        authorizedSubmitters[submitter] = authorized;
        emit SubmitterUpdated(submitter, authorized);
    }

    // ── View Functions ────────────────────────────────────────────────────────

    /**
     * @notice Verify that a price bar's hash matches the on-chain record.
     * @param key          The price record key.
     * @param expectedHash The hash to verify against.
     * @return True if the hash matches the stored record.
     */
    function verifyPrice(bytes32 key, bytes32 expectedHash) external view returns (bool) {
        return records[key].dataHash == expectedHash;
    }

    /**
     * @notice Return the full record for a price key.
     */
    function getRecord(bytes32 key) external view returns (PriceRecord memory) {
        return records[key];
    }

    /**
     * @notice Check whether a key has ever been anchored.
     */
    function isAnchored(bytes32 key) external view returns (bool) {
        return records[key].anchoredAt > 0;
    }
}
