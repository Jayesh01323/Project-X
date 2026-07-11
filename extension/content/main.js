// Project-X Extension Content Script
// Injected into web pages to interact with DOM and page content

console.log('Project-X Extension content script loaded');

// Listen for messages from background or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('Content script received message:', request);
  
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