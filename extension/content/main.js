// Project-X Extension Content Script
// Injected into web pages to interact with DOM and page content

console.log("[Project-X] Content script injected");
console.log('Project-X Extension content script loaded');

// Detect ChatGPT
if (window.location.hostname === 'chatgpt.com' || window.location.hostname === 'chat.openai.com') {
  console.log('[Project-X] ChatGPT detected');
}

// Listen for messages from background or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Content script received message:', request);
  
  if (request.action === 'ping') {
    sendResponse({ success: true, message: 'pong' });
    return true;
  }
  
  if (request.action === 'getPageInfo') {
    // Extract page information
    const pageInfo = {
      url: window.location.href,
      title: document.title,
      timestamp: new Date().toISOString()
    };
    sendResponse({ success: true, data: pageInfo });
    return true;
  }
  
  if (request.action === 'injectScript') {
    // Inject custom scripts into the page
    injectScript(request.script);
    sendResponse({ success: true });
    return true;
  }
  
  return false;
});

// Inject script into page context
function injectScript(scriptContent) {
  const script = document.createElement('script');
  script.textContent = scriptContent;
  script.async = false;
  (document.head || document.documentElement).appendChild(script);
  script.remove();
}

// Example: Observe DOM changes
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.addedNodes.length > 0) {
      // Handle new nodes added to DOM
      console.log('DOM changed:', mutation.addedNodes);
    }
  });
});

// Start observing when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
  });
} else {
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
}

// Example: Intercept fetch requests (optional)
// const originalFetch = window.fetch;
// window.fetch = function(...args) {
//   console.log('Fetch intercepted:', args[0]);
//   return originalFetch.apply(this, args);
// };