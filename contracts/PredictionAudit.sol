// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title PredictionAudit
 * @notice Stores immutable keccak256 hashes of ML prediction snapshots on-chain.
 *
 * Deployed on: Sepolia testnet (development) / Polygon mainnet (production)
 *
 * Purpose:
 *   Provides a tamper-proof, timestamped audit trail of every ML prediction
 *   made by Aegis Analytics AI. Users can independently verify that the model
 *   produced a specific prediction at a given time, using the on-chain hash.
 *
 * Prediction ID derivation (off-chain, in anchor_service.py):
 *   predictionId = keccak256(abi.encodePacked(symbol, ":", horizon, ":", base_ts_utc_iso))
 *
 * Prediction Hash derivation (off-chain, in anchor_service.py):
 *   predictionHash = keccak256(JSON.stringify({symbol, horizon, base_ts_utc,
 *                       expected_return, expected_price, p_up,
 *                       interval_low, interval_high, model_version}))
 */
contract PredictionAudit {
    // ── Storage ───────────────────────────────────────────────────────────────

    struct PredictionRecord {
        bytes32 predictionHash;  // keccak256 of the full canonical prediction JSON
        string  modelVersion;    // e.g. "mvp_v1"
        uint256 anchoredAt;      // block.timestamp when anchored
        address analyst;         // wallet that submitted this prediction
    }

    /// @notice Map from prediction ID → anchored record
    mapping(bytes32 => PredictionRecord) public predictions;

    /// @notice Authorized submitters (Aegis backend signing wallet)
    mapping(address => bool) public authorizedSubmitters;

    address public owner;

    // ── Events ────────────────────────────────────────────────────────────────

    event PredictionAnchored(
        bytes32 indexed predictionId,
        bytes32 indexed predictionHash,
        string  modelVersion,
        uint256 anchoredAt,
        address analyst
    );

    event SubmitterUpdated(address indexed submitter, bool authorized);

    // ── Modifiers ─────────────────────────────────────────────────────────────

    modifier onlyOwner() {
        require(msg.sender == owner, "PredictionAudit: not owner");
        _;
    }

    modifier onlyAuthorized() {
        require(
            authorizedSubmitters[msg.sender] || msg.sender == owner,
            "PredictionAudit: not authorized"
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
     * @notice Anchor a prediction hash on-chain.
     * @param predictionId   Unique ID for this (symbol, horizon, base_ts_utc) tuple.
     * @param predictionHash keccak256 hash of the full prediction JSON payload.
     * @param modelVersion   Human-readable model version string (e.g. "mvp_v1").
     */
    function anchorPrediction(
        bytes32 predictionId,
        bytes32 predictionHash,
        string calldata modelVersion
    ) external onlyAuthorized {
        predictions[predictionId] = PredictionRecord({
            predictionHash: predictionHash,
            modelVersion:   modelVersion,
            anchoredAt:     block.timestamp,
            analyst:        msg.sender
        });

        emit PredictionAnchored(
            predictionId,
            predictionHash,
            modelVersion,
            block.timestamp,
            msg.sender
        );
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
     * @notice Verify that a prediction hash matches the on-chain record.
     * @param predictionId   The prediction record ID.
     * @param expectedHash   The hash to verify against.
     * @return True if the hash matches the stored record.
     */
    function verifyPrediction(
        bytes32 predictionId,
        bytes32 expectedHash
    ) external view returns (bool) {
        return predictions[predictionId].predictionHash == expectedHash;
    }

    /**
     * @notice Return the full record for a prediction ID.
     */
    function getRecord(bytes32 predictionId) external view returns (PredictionRecord memory) {
        return predictions[predictionId];
    }

    /**
     * @notice Check whether a prediction has ever been anchored.
     */
    function isAnchored(bytes32 predictionId) external view returns (bool) {
        return predictions[predictionId].anchoredAt > 0;
    }
}
