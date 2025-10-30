// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./AccessControl.sol";

contract RecordContract {
    AccessControl public acl;

    struct Record {
        address patient;
        address doctor;
        bytes32 sessionId;
        string meta;       // Description of the record (e.g. "Prescription", "Lab Report", etc.)
        uint256 timestamp; // Creation time
    }

    mapping(bytes32 => Record) public records;

    event RecordAdded(
        bytes32 indexed recordKey,
        address indexed patient,
        address indexed doctor,
        bytes32 sessionId,
        string meta,
        uint256 timestamp
    );

    constructor(address _accessControl) {
        require(_accessControl != address(0), "Invalid AccessControl address");
        acl = AccessControl(_accessControl);
    }

    /// @notice Compute a unique record key using patient, doctor, and sessionId.
    function computeRecordKey(
        address patient,
        address doctor,
        bytes32 sessionId
    ) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(patient, doctor, sessionId));
    }

    /// @notice Allows a doctor to add a medical record linked to a patient and session.
    function addRecord(
        address patient,
        bytes32 sessionId,
        string calldata meta
    ) external {
        require(acl.isDoctor(msg.sender), "Only doctor can add record");
        require(acl.isPatient(patient), "Target not a registered patient");

        bytes32 recordKey = computeRecordKey(patient, msg.sender, sessionId);
        Record storage r = records[recordKey];
        require(r.timestamp == 0, "Record already exists");

        r.patient = patient;
        r.doctor = msg.sender;
        r.sessionId = sessionId;
        r.meta = meta;
        r.timestamp = block.timestamp;

        emit RecordAdded(recordKey, patient, msg.sender, sessionId, meta, block.timestamp);
    }

    /// @notice Retrieve a specific record by its recordKey.
    function getRecord(bytes32 recordKey) external view returns (Record memory) {
        return records[recordKey];
    }

    /// @notice Check if a record exists for a given combination of patient, doctor, and session.
    function recordExists(
        address patient,
        address doctor,
        bytes32 sessionId
    ) external view returns (bool) {
        bytes32 key = computeRecordKey(patient, doctor, sessionId);
        return records[key].timestamp != 0;
    }
}
