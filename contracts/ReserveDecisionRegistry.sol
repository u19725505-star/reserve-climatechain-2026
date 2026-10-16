// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title RESERVE Decision Evidence Registry
/// @notice Stores hashes and sequence links for off-chain RESERVE decision records.
/// @dev Prototype contract. Deploy and audit on a chosen testnet before claiming
///      a live blockchain integration. Never store shipment PII or raw operational
///      records on-chain; submit only a digest and non-sensitive version hashes.
contract ReserveDecisionRegistry {
    struct DecisionRecord {
        uint64 sequence;
        bytes32 recordHash;
        bytes32 previousHash;
        bytes32 modelVersionHash;
        uint64 recordedAt;
        address submitter;
    }

    address public owner;
    mapping(address => bool) public authorizedWriters;
    mapping(uint64 => DecisionRecord) private records;
    uint64 public recordCount;
    bytes32 public latestRecordHash;

    event WriterAuthorizationChanged(address indexed writer, bool authorized);
    event DecisionAnchored(
        uint64 indexed sequence,
        bytes32 indexed recordHash,
        bytes32 previousHash,
        bytes32 modelVersionHash,
        address indexed submitter,
        uint64 recordedAt
    );

    error Unauthorized();
    error ZeroHash();
    error PreviousHashMismatch(bytes32 expected, bytes32 supplied);
    error InvalidOwner();

    constructor() {
        owner = msg.sender;
        authorizedWriters[msg.sender] = true;
        emit WriterAuthorizationChanged(msg.sender, true);
    }

    modifier onlyOwner() {
        if (msg.sender != owner) revert Unauthorized();
        _;
    }

    modifier onlyWriter() {
        if (!authorizedWriters[msg.sender]) revert Unauthorized();
        _;
    }

    function setWriter(address writer, bool authorized) external onlyOwner {
        if (writer == address(0)) revert InvalidOwner();
        authorizedWriters[writer] = authorized;
        emit WriterAuthorizationChanged(writer, authorized);
    }

    /// @param recordHash SHA-256 or keccak256 digest of a canonical off-chain record.
    /// @param previousHash Hash of the previously anchored record; zero for genesis.
    /// @param modelVersionHash Digest of model version/configuration metadata.
    function anchorDecision(
        bytes32 recordHash,
        bytes32 previousHash,
        bytes32 modelVersionHash
    ) external onlyWriter returns (uint64 sequence) {
        if (recordHash == bytes32(0) || modelVersionHash == bytes32(0)) revert ZeroHash();
        if (previousHash != latestRecordHash) {
            revert PreviousHashMismatch(latestRecordHash, previousHash);
        }

        sequence = recordCount + 1;
        uint64 timestamp = uint64(block.timestamp);
        records[sequence] = DecisionRecord({
            sequence: sequence,
            recordHash: recordHash,
            previousHash: previousHash,
            modelVersionHash: modelVersionHash,
            recordedAt: timestamp,
            submitter: msg.sender
        });
        recordCount = sequence;
        latestRecordHash = recordHash;

        emit DecisionAnchored(
            sequence, recordHash, previousHash, modelVersionHash, msg.sender, timestamp
        );
    }

    function getRecord(uint64 sequence) external view returns (DecisionRecord memory) {
        require(sequence > 0 && sequence <= recordCount, "record does not exist");
        return records[sequence];
    }
}
