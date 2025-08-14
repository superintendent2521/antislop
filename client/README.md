# Anti-Slop YouTube Blocker - Firefox Extension

A Firefox extension that automatically blocks YouTube videos marked as AI-generated slop content by checking against the Anti-Slop API.

## Features

- **Automatic blocking**: Checks every YouTube video URL you visit
- **Real-time API integration**: Connects to your local Anti-Slop API
- **Clean blocked page**: Shows a professional "video blocked" message
- **Caching**: Reduces API calls by caching results for 5 minutes
- **Popup interface**: Shows extension status and connection health

## Installation

1. **Prerequisites**: Ensure your Anti-Slop API server is running on `http://localhost:8000`

2. **Load the extension in Firefox**:
   - Open Firefox and navigate to `about:debugging`
   - Click "This Firefox"
   - Click "Load Temporary Add-on"
   - Navigate to the `client` folder and select `manifest.json`

3. **Verify installation**:
   - Click the extension icon in Firefox toolbar
   - You should see the popup showing "Connected" status

## Usage

1. **Automatic blocking**: Simply browse YouTube as normal
2. **When blocked**: You'll be redirected to a local page indicating the video is AI slop
3. **Extension popup**: Click the extension icon to see connection status

## File Structure

```
client/
├── manifest.json          # Extension manifest
├── background.js          # Background service worker
├── content.js            # Content script for YouTube pages
├── blocked.html          # Blocked video page
├── blocked.css           # Styles for blocked page
├── blocked.js            # Script for blocked page
├── popup.html            # Extension popup
├── popup.js              # Popup script
└── README.md             # This file
```

## API Endpoints Used

- `GET /check_video/{video_id}` - Check if a video is blocked
- `GET /health` - Check API health status

## Development

### Testing the extension

1. Start your Anti-Slop API server:
   ```bash
   python main.py
   ```

2. Load the extension in Firefox as described above

3. Visit a YouTube video URL to test blocking

### Making changes

1. Edit files in the `client` directory
2. Reload the extension in Firefox:
   - Go to `about:debugging`
   - Find your extension and click "Reload"

## Troubleshooting

### Extension not working
- Ensure the API server is running on `http://localhost:8000`
- Check browser console for errors (F12 → Console tab)
- Verify extension permissions are granted

### API connection issues
- Check if the API server is accessible at `http://localhost:8000/health`
- Ensure CORS is properly configured on the API server
- Check firewall settings

### Videos not being blocked
- Verify the video ID exists in your blocked videos database
- Check the API response for the specific video ID
- Clear extension cache by reloading the extension

## Permissions Required

- `activeTab`: To access current YouTube page
- `storage`: To store blocked video cache
- `webRequest`: To intercept YouTube requests
- `*://*.youtube.com/*`: To run on YouTube pages

## Security Notes

- The extension only communicates with your local API server
- No data is sent to external servers
- All blocking decisions are made by your local API
