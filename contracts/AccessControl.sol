// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/// @title Enhanced Access Control for SwasthyaLink
/// @notice Adds optional metadata for doctors and patients (name, specialization, gender, age)
contract AccessControl {
    address public admin;

    mapping(address => bool) public isDoctor;
    mapping(address => bool) public isPatient;

    // Store details separately
    struct Doctor {
        string name;
        string specialization;
    }

    struct Patient {
        string name;
        string gender;
        uint8 age;
    }

    mapping(address => Doctor) public doctorDetails;
    mapping(address => Patient) public patientDetails;

    event DoctorRegistered(address indexed doctor);
    event DoctorRevoked(address indexed doctor);
    event PatientRegistered(address indexed patient);
    event PatientRevoked(address indexed patient);
    event AdminTransferred(address indexed previousAdmin, address indexed newAdmin);

    modifier onlyAdmin() {
        require(msg.sender == admin, "AccessControl: admin only");
        _;
    }

    modifier onlyDoctor() {
        require(isDoctor[msg.sender], "AccessControl: doctor only");
        _;
    }

    modifier onlyPatient() {
        require(isPatient[msg.sender], "AccessControl: patient only");
        _;
    }

    constructor(address _initialAdmin) {
        require(_initialAdmin != address(0), "Admin cannot be zero");
        admin = _initialAdmin;
        emit AdminTransferred(address(0), _initialAdmin);
    }

    // Admin management
    function transferAdmin(address _newAdmin) external onlyAdmin {
        require(_newAdmin != address(0), "new admin zero");
        emit AdminTransferred(admin, _newAdmin);
        admin = _newAdmin;
    }

    // Basic registration (only address)
    function registerDoctor(address _doctor) external onlyAdmin {
        require(_doctor != address(0), "zero address");
        require(!isDoctor[_doctor], "already doctor");
        isDoctor[_doctor] = true;
        emit DoctorRegistered(_doctor);
    }

    function registerPatient(address _patient) external onlyAdmin {
        require(_patient != address(0), "zero address");
        require(!isPatient[_patient], "already patient");
        isPatient[_patient] = true;
        emit PatientRegistered(_patient);
    }

    // Add or update metadata separately
    function updateDoctorDetails(address _doctor, string memory _name, string memory _specialization) external onlyAdmin {
        require(isDoctor[_doctor], "not registered doctor");
        doctorDetails[_doctor] = Doctor(_name, _specialization);
    }

    function updatePatientDetails(address _patient, string memory _name, string memory _gender, uint8 _age) external onlyAdmin {
        require(isPatient[_patient], "not registered patient");
        patientDetails[_patient] = Patient(_name, _gender, _age);
    }

    // Revocations
    function revokeDoctor(address _doctor) external onlyAdmin {
        require(isDoctor[_doctor], "not a doctor");
        isDoctor[_doctor] = false;
        emit DoctorRevoked(_doctor);
    }

    function revokePatient(address _patient) external onlyAdmin {
        require(isPatient[_patient], "not a patient");
        isPatient[_patient] = false;
        emit PatientRevoked(_patient);
    }
}
