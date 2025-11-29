import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

// Get API host and port from environment variables
// REACT_APP_API_HOST: The IP address or hostname of the backend server (default: localhost)
// REACT_APP_API_PORT: The port where the backend is running (default: 13579)
const API_HOST = process.env.REACT_APP_API_HOST || 'localhost';
const API_PORT = process.env.REACT_APP_API_PORT || 13579;
const API_BASE_URL = `http://${API_HOST}:${API_PORT}`;

function App() {
  const [status, setStatus] = useState("Checking...");
  const [statusType, setStatusType] = useState("checking");
  const [lastAction, setLastAction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState(() => {
    // Get theme from localStorage or default to dark
    const savedTheme = localStorage.getItem('theme');
    return savedTheme || 'dark';
  });

  // Apply theme to document
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'dark' ? 'light' : 'dark');
  };

  const fetchStatus = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/status`);
      if (res.data.online) {
        setStatus("Online");
        setStatusType("online");
      } else {
        setStatus("Offline");
        setStatusType("offline");
      }
    } catch (error) {
      setStatus("Connection Error");
      setStatusType("error");
    }
  };

  const action = async (cmd) => {
    setLoading(true);
    setLastAction(cmd);
    try {
      await axios.get(`${API_BASE_URL}/${cmd}`);
      // Immediately check status after button press
      await fetchStatus();
      setLoading(false);
    } catch (error) {
      setStatus("Action Failed");
      setStatusType("error");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    // Check status every 10 seconds
    const interval = setInterval(fetchStatus, 10000);
    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = () => {
    switch (statusType) {
      case "online":
        return "●";
      case "offline":
        return "●";
      case "error":
        return "⚠";
      default:
        return "◐";
    }
  };

  return (
    <div className="App">
      <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme" title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}>
        <svg className="theme-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          {theme === 'dark' ? (
            <>
              <circle cx="12" cy="12" r="5"></circle>
              <line x1="12" y1="1" x2="12" y2="3"></line>
              <line x1="12" y1="21" x2="12" y2="23"></line>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
              <line x1="1" y1="12" x2="3" y2="12"></line>
              <line x1="21" y1="12" x2="23" y2="12"></line>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </>
          ) : (
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          )}
        </svg>
      </button>
      <div className="container">
        <h1>DKC Wake-On-Lan</h1>
        <div className="status-container">
          <div className="status-label">System Status</div>
          <div className={`status ${statusType}`}>
            <span>{getStatusIcon()}</span>
            <span>{status}</span>
          </div>
        </div>
        <div className="buttons">
          <button
            className="start"
            onClick={() => action("start")}
            disabled={loading || statusType === "online"}
          >
            {loading && lastAction === "start" ? "Starting..." : "Start System"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
