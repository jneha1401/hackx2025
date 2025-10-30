import React, { useState } from 'react';

const App = () => {
  const [currentView, setCurrentView] = useState('landing');
  const [userRole, setUserRole] = useState('patient');
  const [currentLanguage, setCurrentLanguage] = useState('en');
  const [username, setUsername] = useState('');

  const translations = {
    en: { welcome: 'Welcome!', consult: 'Consult', records: 'Records', call: 'Call', sendMsg: 'Send Message', back: 'Back', logout: 'Logout', prescriptions: 'Prescriptions', inbox: 'Inbox', pastRecords: 'Past Records' },
    hi: { welcome: 'स्वागत है!', consult: 'परामर्श', records: 'रिकॉर्ड', call: 'कॉल', sendMsg: 'संदेश भेजें', back: 'वापस', logout: 'लॉगआउट', prescriptions: 'पर्चे', inbox: 'इनबॉक्स', pastRecords: 'पिछले रिकॉर्ड' },
    mr: { welcome: 'स्वागत आहे!', consult: 'सल्ला', records: 'नोंदी', call: 'कॉल', sendMsg: 'संदेश पाठवा', back: 'मागे', logout: 'लॉगआउट', prescriptions: 'औषधाचे प्रिस्क्रिप्शन', inbox: 'इनबॉक्स', pastRecords: 'मागील नोंदी' },
    kn: { welcome: 'ಸ್ವಾಗತ!', consult: 'ಸಮಾಲೋಚನೆ', records: 'ದಾಖಲೆಗಳು', call: 'ಕಾಲ್', sendMsg: 'ಸಂದೇಶ ಕಳುಹಿಸಿ', back: 'ಹಿಂದೆ', logout: 'ಲಾಗ್ಔಟ್', prescriptions: 'ಔಷಧ ಪತ್ರ', inbox: 'ಇನ್‌ಬಾಕ್ಸ್', pastRecords: 'ಹಿಂದಿನ ದಾಖಲೆಗಳು' }
  };

  const t = translations[currentLanguage];

  const login = () => {
    setCurrentView(userRole === 'patient' ? 'patientDashboard' : 'doctorDashboard');
  };

  const logout = () => {
    setCurrentView('landing');
  };

  const openSection = (section) => {
    setCurrentView(section);
  };

  const backToDashboard = (role) => {
    setCurrentView(role === 'patient' ? 'patientDashboard' : 'doctorDashboard');
  };

  const translate = (lang) => {
    setCurrentLanguage(lang);
  };

  const startCall = () => {
    setCurrentView('callPage');
    
    setTimeout(() => {
      const roomID = Math.floor(Math.random() * 10000) + "";
      const userID = Math.floor(Math.random() * 10000) + "";
      const userName = "userName" + userID;
      const appID = 874004200;
      const serverSecret = "47fb38e893493cec2b9fcd37e7f1e7ed";
      
      if (window.ZegoUIKitPrebuilt) {
        const kitToken = window.ZegoUIKitPrebuilt.generateKitTokenForTest(appID, serverSecret, roomID, userID, userName);
        const zp = window.ZegoUIKitPrebuilt.create(kitToken);
        zp.joinRoom({
          container: document.querySelector("#zego-root"),
          sharedLinks: [{
            name: 'Personal link',
            url: window.location.protocol + '//' + window.location.host + window.location.pathname + '?roomID=' + roomID,
          }],
          scenario: {
            mode: window.ZegoUIKitPrebuilt.VideoConference,
          },
          turnOnMicrophoneWhenJoining: true,
          turnOnCameraWhenJoining: true,
          showMyCameraToggleButton: true,
          showMyMicrophoneToggleButton: true,
          showAudioVideoSettingsButton: true,
          showScreenSharingButton: true,
          showTextChat: true,
          showUserList: true,
          maxUsers: 2,
          layout: 'Auto',
          showLayoutButton: false,
        });
      }
    }, 100);
  };

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#001b3f', color: 'white', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', margin: 0, fontFamily: "'Nunito', sans-serif" }}>
      
      {/* Landing Page */}
      {currentView === 'landing' && (
        <div id="landingPage">
          <div className="logo-container">
            <img src="https://i.ibb.co/V00hmTP2/logo.png" alt="SwasthyaLink Logo" />
          </div>
          <div className="login-container">
            <input 
              type="text" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter Your Name" 
            />
            <select value={userRole} onChange={(e) => setUserRole(e.target.value)}>
              <option value="patient">Patient</option>
              <option value="doctor">Doctor</option>
            </select>
            <select value={currentLanguage} onChange={(e) => translate(e.target.value)}>
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="mr">Marathi</option>
              <option value="kn">Kannada</option>
            </select>
            <button className="btn" onClick={login}>Login</button>
          </div>
        </div>
      )}

      {/* Patient Dashboard */}
      {currentView === 'patientDashboard' && (
        <div className="container">
          <h2>{t.welcome}</h2>
          <div className="grid">
            <div className="card" onClick={() => openSection('consultPatient')}>
              <i className="fas fa-stethoscope icon"></i>
              <h3>{t.consult}</h3>
            </div>
            <div className="card" onClick={() => openSection('recordsPatient')}>
              <i className="fas fa-file-medical icon"></i>
              <h3>{t.records}</h3>
            </div>
          </div>
          <button className="btn" onClick={logout}>{t.logout}</button>
        </div>
      )}

      {/* Doctor Dashboard */}
      {currentView === 'doctorDashboard' && (
        <div className="container">
          <h2>{t.welcome}</h2>
          <div className="grid">
            <div className="card" onClick={() => openSection('consultDoctor')}>
              <i className="fas fa-user-md icon"></i>
              <h3>{t.consult}</h3>
            </div>
            <div className="card" onClick={() => openSection('recordsDoctor')}>
              <i className="fas fa-folder-open icon"></i>
              <h3>{t.records}</h3>
            </div>
          </div>
          <button className="btn" onClick={logout}>{t.logout}</button>
        </div>
      )}

      {/* Consult Patient */}
      {currentView === 'consultPatient' && (
        <div className="container">
          <h2>{t.consult}</h2>
          <div className="grid">
            <div className="card" onClick={startCall}>
              <i className="fas fa-phone icon"></i>
              <h3>{t.call}</h3>
            </div>
            <div className="card">
              <i className="fas fa-comment-dots icon"></i>
              <h3>{t.sendMsg}</h3>
            </div>
          </div>
          <button className="btn" onClick={() => backToDashboard('patient')}>{t.back}</button>
        </div>
      )}

      {/* Consult Doctor */}
      {currentView === 'consultDoctor' && (
        <div className="container">
          <h2>{t.consult}</h2>
          <div className="grid">
            <div className="card" onClick={startCall}>
              <i className="fas fa-phone icon"></i>
              <h3>{t.call}</h3>
            </div>
            <div className="card">
              <i className="fas fa-comment-dots icon"></i>
              <h3>{t.sendMsg}</h3>
            </div>
          </div>
          <button className="btn" onClick={() => backToDashboard('doctor')}>{t.back}</button>
        </div>
      )}

      {/* Records Patient */}
      {currentView === 'recordsPatient' && (
        <div className="container">
          <h2>{t.records}</h2>
          <div className="grid">
            <div className="card">
              <i className="fas fa-prescription-bottle-alt icon"></i>
              <h3>{t.prescriptions}</h3>
            </div>
            <div className="card">
              <i className="fas fa-envelope icon"></i>
              <h3>{t.inbox}</h3>
            </div>
          </div>
          <button className="btn" onClick={() => backToDashboard('patient')}>{t.back}</button>
        </div>
      )}

      {/* Records Doctor */}
      {currentView === 'recordsDoctor' && (
        <div className="container">
          <h2>{t.records}</h2>
          <div className="grid">
            <div className="card">
              <i className="fas fa-clipboard-list icon"></i>
              <h3>{t.pastRecords}</h3>
            </div>
          </div>
          <button className="btn" onClick={() => backToDashboard('doctor')}>{t.back}</button>
        </div>
      )}

      {/* Call Page */}
      {currentView === 'callPage' && (
        <div id="callPage" style={{ width: '100vw', height: '100vh' }}>
          <div id="zego-root" style={{ width: '100%', height: '100%' }}></div>
        </div>
      )}
    </div>
  );
};

export default App;
