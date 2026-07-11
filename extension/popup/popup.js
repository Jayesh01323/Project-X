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
    const apiUrl = result.apiUrl || 'http://localhost:8000/api/v1';
    
    updateStatus(settings.enabled);
    
    // Check backend connection
    await checkBackendConnection(apiUrl);
  } catch (error) {
    console.error('Error initializing popup:', error);
    updateStatus(false);
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

// Check backend connection
async function checkBackendConnection(apiUrl) {
  try {
    const response = await fetch(`${apiUrl}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    if (response.ok) {
      console.log('Backend connection successful');
    } else {
      console.warn('Backend returned non-ok status:', response.status);
    }
  } catch (error) {
    console.warn('Backend connection failed:', error);
    // Backend might not be running, which is fine for foundation
  }
}

// Handle refresh button click
async function handleRefresh() {
  const refreshBtn = document.getElementById('refreshBtn');
  refreshBtn.disabled = true;
  refreshBtn.textContent = 'Refreshing...';
  
  try {
    // Request page info from content script
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    if (tab && tab.id) {
      chrome.tabs.sendMessage(tab.id, { action: 'getPageInfo' }, (response) => {
        if (response && response.success) {
          document.getElementById('pageUrl').textContent = response.data.url;
          document.getElementById('pageTitle').textContent = response.data.title;
        }
      });
    }
  } catch (error) {
    console.error('Error refreshing:', error);
  } finally {
    refreshBtn.disabled = false;
    refreshBtn.textContent = 'Refresh';
  }
}

// Handle settings button click
function handleSettings() {
  // Open options page or show settings modal
  if (chrome.runtime.openOptionsPage) {
    chrome.runtime.openOptionsPage();
  } else {
    // Fallback: open a new tab with settings
    chrome.tabs.create({ url: 'options.html' });
  }
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