// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "./AccessControl.sol";

/// @title ConsentContract for SwasthyaLink
/// @notice Handles patient consent for sharing medical records with doctors.
contract ConsentContract {
    AccessControl public acl;

    struct Consent {
        address patient;
        address doctor;
        bytes32 sessionId;
        bytes32 dataHash; // hash of patient’s message or context
        bool active;
        uint256 timestamp;
    }

    // consentKey => Consent
    mapping(bytes32 => Consent) public consents;

    event ConsentGiven(
        address indexed patient,
        address indexed doctor,
        bytes32 indexed sessionId,
        bytes32 dataHash,
        uint256 timestamp
    );

    event ConsentRevoked(
        address indexed patient,
        address indexed doctor,
        bytes32 indexed sessionId,
        uint256 timestamp
    );

    constructor(address _acl) {
        require(_acl != address(0), "invalid ACL address");
        acl = AccessControl(_acl);
    }

    /// @notice Give consent to a doctor for a session
    /// @param doctor Address of the doctor
    /// @param dataDescription Short description (string provided by patient)
    /// @param patientInput Optional patient-provided text (will be hashed)
    function giveConsent(
        address doctor,
        string calldata dataDescription,
        string calldata patientInput
    ) external {
        require(acl.isPatient(msg.sender), "Not a registered patient");
        require(acl.isDoctor(doctor), "Target not a registered doctor");

        bytes32 sessionId = keccak256(abi.encodePacked(msg.sender, doctor, block.timestamp));
        bytes32 dataHash = keccak256(abi.encodePacked(dataDescription, patientInput));

        bytes32 consentKey = keccak256(abi.encodePacked(msg.sender, doctor, sessionId));

        consents[consentKey] = Consent({
            patient: msg.sender,
            doctor: doctor,
            sessionId: sessionId,
            dataHash: dataHash,
            active: true,
            timestamp: block.timestamp
        });

        emit ConsentGiven(msg.sender, doctor, sessionId, dataHash, block.timestamp);
    }

    /// @notice Revoke consent for a given session
    function revokeConsent(bytes32 sessionId, address doctor) external {
        bytes32 consentKey = keccak256(abi.encodePacked(msg.sender, doctor, sessionId));
        Consent storage c = consents[consentKey];
        require(c.patient == msg.sender, "Not consent owner");
        require(c.active, "Consent already inactive");

        c.active = false;
        emit ConsentRevoked(msg.sender, doctor, sessionId, block.timestamp);
    }

    /// ✅ Reintroduced helper: check if consent is active
    function isConsentActive(bytes32 consentKey) public view returns (bool) {
        return consents[consentKey].active;
    }
}
