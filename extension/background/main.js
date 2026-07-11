// Project-X Extension Background Service Worker
// Handles background tasks and event listeners

console.log('Project-X Extension background service worker initialized');

// Listen for extension installation
chrome.runtime.onInstalled.addListener((details) => {
  console.log('Extension installed:', details.reason);
  
  if (details.reason === 'install') {
    // Initialize default settings
    chrome.storage.local.set({
      apiUrl: 'http://localhost:8000/api/v1',
      settings: {
        enabled: true,
        notifications: true
      }
    });
  }
});

// Listen for messages from content scripts or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Message received:', request);
  
  if (request.action === 'fetchData') {
    // Handle API requests from extension
    handleApiRequest(request)
      .then(data => sendResponse({ success: true, data }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Indicates async response
  }
  
  return false;
});

// Handle API requests
async function handleApiRequest(request) {
  const { url, options = {} } = request;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

// Example: Periodic background task (optional)
// chrome.alarms.create('sync', { periodInMinutes: 5 });
// chrome.alarms.onAlarm.addListener((alarm) => {
//   if (alarm.name === 'sync') {
//     // Perform periodic sync
//   }
// });