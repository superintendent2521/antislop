// Content script that runs on YouTube pages
(function() {
  'use strict';
  
  // Extract video ID from URL
  function getVideoIdFromUrl(url) {
    const urlObj = new URL(url);
    return urlObj.searchParams.get('v');
  }
  
  // Check if current page is a video page
  function isVideoPage() {
    const url = window.location.href;
    return url.includes('youtube.com/watch') && getVideoIdFromUrl(url);
  }
  
  // Get current video ID
  function getCurrentVideoId() {
    return getVideoIdFromUrl(window.location.href);
  }
  
  // Redirect to blocked page
  function redirectToBlockedPage(videoId) {
    const blockedUrl = chrome.runtime.getURL('blocked.html') + '?videoId=' + encodeURIComponent(videoId);
    window.location.replace(blockedUrl);
  }
  
  // Check if video is blocked
  async function checkAndBlockVideo() {
    if (!isVideoPage()) return;
    
    const videoId = getCurrentVideoId();
    if (!videoId) return;
    
    try {
      const response = await chrome.runtime.sendMessage({
        action: 'checkVideo',
        videoId: videoId
      });
      
      if (response && response.isBlocked) {
        redirectToBlockedPage(videoId);
      }
    } catch (error) {
      console.error('Error checking video:', error);
    }
  }
  
  // Monitor URL changes for SPA navigation
  let lastUrl = location.href;
  new MutationObserver(() => {
    const url = location.href;
    if (url !== lastUrl) {
      lastUrl = url;
      checkAndBlockVideo();
    }
  }).observe(document, { subtree: true, childList: true });
  
  // Check on initial load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkAndBlockVideo);
  } else {
    checkAndBlockVideo();
  }
})();
