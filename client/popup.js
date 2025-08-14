// Popup script for extension popup
document.addEventListener('DOMContentLoaded', async function() {
    const apiStatus = document.getElementById('api-status');
    const blockedCount = document.getElementById('blocked-count');
    
    // Check API connection
    try {
        const response = await fetch('http://localhost:8000/', {
            method: 'GET',
            signal: AbortSignal.timeout(2000)
        });
        
        if (response.ok) {
            apiStatus.textContent = 'Connected';
            apiStatus.className = 'status-value active';
        } else {
            apiStatus.textContent = 'Error';
            apiStatus.className = 'status-value blocked';
        }
    } catch (error) {
        apiStatus.textContent = 'Offline';
        apiStatus.className = 'status-value blocked';
    }
    
    // Get blocked count from storage
    chrome.storage.local.get(['blockedCount'], function(result) {
        blockedCount.textContent = result.blockedCount || 0;
    });
});
