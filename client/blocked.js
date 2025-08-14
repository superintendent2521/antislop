// Script for the blocked page
document.addEventListener('DOMContentLoaded', function() {
    // Get video ID from URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const videoId = urlParams.get('videoId');
    
    // Display video ID
    const videoIdElement = document.getElementById('video-id');
    if (videoIdElement && videoId) {
        videoIdElement.textContent = videoId;
    }
    
    // Go back button functionality
    const goBackBtn = document.getElementById('go-back-btn');
    if (goBackBtn) {
        goBackBtn.addEventListener('click', function() {
            if (document.referrer && document.referrer.includes('youtube.com')) {
                window.history.back();
            } else {
                window.location.href = 'https://www.youtube.com';
            }
        });
    }
    
    // Home button functionality
    const homeBtn = document.getElementById('home-btn');
    if (homeBtn) {
        homeBtn.addEventListener('click', function() {
            window.location.href = 'https://www.youtube.com';
        });
    }
});
