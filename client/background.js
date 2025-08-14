// Background script for handling API calls and storage
const API_BASE_URL = 'http://localhost:8000';

// Cache for blocked video IDs to reduce API calls
let blockedVideosCache = new Set();
let cacheTimestamp = 0;
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

// Check if a video is blocked via API
async function checkVideoBlocked(videoId) {
  try {
    // Check cache first
    if (Date.now() - cacheTimestamp < CACHE_DURATION) {
      if (blockedVideosCache.has(videoId)) {
        return true;
      }
    }
    
    // Fetch from API
    const response = await fetch(`${API_BASE_URL}/api/videos/${videoId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    
    if (response.ok) {
      const data = await response.json();
      if (data.blocked) {
        blockedVideosCache.add(videoId);
        cacheTimestamp = Date.now();
        return true;
      }
    }
    
    return false;
  } catch (error) {
    console.error('Error checking video:', error);
    return false;
  }
}

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'checkVideo') {
    checkVideoBlocked(request.videoId)
      .then(isBlocked => sendResponse({ isBlocked }))
      .catch(error => {
        console.error('Error in background script:', error);
        sendResponse({ isBlocked: false });
      });
    return true; // Keep message channel open for async response
  }
});

// Clear cache periodically
setInterval(() => {
  blockedVideosCache.clear();
  cacheTimestamp = 0;
}, CACHE_DURATION);
