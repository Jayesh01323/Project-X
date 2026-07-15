// Project-X Extension Popup Script
// Handles popup UI interactions

document.addEventListener('DOMContentLoaded', async () => {
  console.log('Project-X Extension popup loaded');
  
  // Get DOM elements
  const statusIndicator = document.getElementById('statusIndicator');
  const statusText = document.getElementById('statusText');
  const pageUrl = document.getElementById('pageUrl');
  const pageTitle = document.getElementById('pageTitle');
  const refreshBtn = document.getElementById('refreshBtn');
  const settingsBtn = document.getElementById('settingsBtn');
  
  // Initialize popup
  await initializePopup();
  
  // Event listeners
  refreshBtn.addEventListener('click', handleRefresh);
  settingsBtn.addEventListener('click', handleSettings);
  
  // Get current tab information
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab) {
      pageUrl.textContent = tab.url || '-';
      pageTitle.textContent = tab.title || '-';
    }
  } catch (error) {
    console.error('Error getting tab info:', error);
    pageUrl.textContent = 'Error loading';
    pageTitle.textContent = 'Error loading';
  }
});

// Initialize popup with stored settings
async function initializePopup() {
  try {
    const result = await chrome.storage.local.get(['settings', 'apiUrl']);
    const settings = result.settings || { enabled: true, notifications: true };
    const apiUrl = result.apiUrl || 'http://127.0.0.1:8000/api/v1';
    
    await checkBackendConnection(apiUrl);
  } catch (error) {
    console.error('Error initializing popup:', error);
    updateBackendStatus(false);
  }
}

// Update status indicator
function updateStatus(isEnabled) {
  const statusIndicator = document.getElementById('statusIndicator');
  const statusText = document.getElementById('statusText');
  
  if (isEnabled) {
    statusIndicator.classList.add('active');
    statusText.textContent = 'Active';
  } else {
    statusIndicator.classList.add('inactive');
    statusText.textContent = 'Inactive';
  }
}

// Update backend status
function updateBackendStatus(isConnected) {
  const statusIndicator = document.getElementById('statusIndicator');
  const statusText = document.getElementById('statusText');
  
  if (isConnected) {
    statusIndicator.classList.add('active');
    statusIndicator.classList.remove('inactive');
    statusText.textContent = '🟢 Backend Connected';
  } else {
    statusIndicator.classList.add('inactive');
    statusIndicator.classList.remove('active');
    statusText.textContent = '🔴 Backend Offline';
  }
}

// Check backend connection
async function checkBackendConnection(apiUrl) {
  try {
    const response = await fetch('http://127.0.0.1:8000/health', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      updateBackendStatus(true);
    } else {
      updateBackendStatus(false);
    }
  } catch (error) {
    updateBackendStatus(false);
  }
}

// Handle refresh button click
async function handleRefresh() {
  const refreshBtn = document.getElementById('refreshBtn');
  refreshBtn.disabled = true;
  refreshBtn.textContent = 'Refreshing...';
  
  try {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    console.log("[Project-X] Sending ping to tab:", tab.id, "URL:", tab.url);
    
    if (tab && tab.id) {
      chrome.tabs.sendMessage(tab.id, { action: "ping" }, (response) => {
        console.log("[Project-X] Response received:", response);
        console.log("[Project-X] chrome.runtime.lastError:", chrome.runtime.lastError);
        
        if (chrome.runtime.lastError) {
            console.warn("Content script unavailable:", chrome.runtime.lastError.message);
            return;
        }

        if (response?.success && response.message === "pong") {
            console.log("Received: pong");
        } else {
            console.warn("Unexpected response:", response);
        }
      });
    }
  } catch (error) {
    console.warn('Content script unavailable');
  } finally {
    refreshBtn.disabled = false;
    refreshBtn.textContent = 'Refresh';
  }
}

// Handle settings button click
function handleSettings() {
  chrome.runtime.sendMessage({ action: "backgroundPing" }, (response) => {
    if (chrome.runtime.lastError) {
      console.warn("Background unavailable:", chrome.runtime.lastError.message);
      return;
    }

    if (response?.success && response.message === "background-pong") {
      console.log("Received: background-pong");
    } else {
      console.warn("Unexpected response:", response);
    }
  });
}

// Example: Send message to background
async function sendMessageToBackground(action, data = {}) {
  try {
    const response = await chrome.runtime.sendMessage({
      action,
      ...data
    });
    return response;
  } catch (error) {
    console.error('Error sending message to background:', error);
    throw error;
  }
}