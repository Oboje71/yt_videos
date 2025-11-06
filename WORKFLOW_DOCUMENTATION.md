# YouTube Content Automation Workflow - Documentation

## Overview

This n8n workflow automates the entire process of converting YouTube videos into multi-platform social media content. It extracts transcripts, identifies engaging hooks using AI, generates platform-specific posts, creates short-form videos, and delivers everything to clients via Google Drive.

## Workflow Features

### What This Workflow Does:

1. **Receives YouTube Links** - Via webhook endpoint
2. **Extracts Transcripts** - Using RapidAPI's YouTube Transcript API
3. **Identifies Content Hooks** - ChatGPT analyzes transcript for engaging moments
4. **Generates Social Media Posts**:
   - X (Twitter): 3 engaging posts with hashtags
   - LinkedIn: 2 professional posts
   - Instagram: 2 captions with hashtags
5. **Creates Short Videos** - Using Vizard AI for auto-generated shorts
6. **Saves to Google Drive** - Organized folder with all content
7. **Emails Client** - Beautiful HTML email with Google Drive link

## Setup Instructions

### Prerequisites

- n8n instance (self-hosted or cloud)
- API Keys for:
  - RapidAPI (YouTube Transcript API)
  - OpenAI (GPT-4)
  - Vizard AI
  - Google Drive OAuth2
  - SMTP Email Account

### Step 1: Install the Workflow

1. Open your n8n instance
2. Click on "Workflows" → "Import from File"
3. Select `youtube-content-automation-workflow.json`
4. The workflow will be imported with all nodes

### Step 2: Configure Environment Variables

Set up the following environment variables in n8n:

```bash
RAPIDAPI_KEY=your_rapidapi_key_here
VIZARD_API_KEY=your_vizard_api_key_here
SENDER_EMAIL=your_email@domain.com
```

You can set these in:
- n8n Cloud: Settings → Environments
- Self-hosted: Add to your `.env` file or docker-compose environment section

### Step 3: Configure Credentials

You need to set up the following credentials in n8n:

#### 1. OpenAI API
- Go to Settings → Credentials → New
- Select "OpenAI API"
- Add your OpenAI API key
- Name it: "OpenAI API"

#### 2. Google Drive OAuth2
- Go to Settings → Credentials → New
- Select "Google Drive OAuth2 API"
- Follow the OAuth flow to connect your Google account
- Name it: "Google Drive OAuth2"

#### 3. SMTP Email
- Go to Settings → Credentials → New
- Select "SMTP"
- Configure your email provider settings:
  - Gmail: smtp.gmail.com, port 587, TLS
  - Outlook: smtp.office365.com, port 587, STARTTLS
  - Custom SMTP: your provider settings
- Name it: "SMTP Account"

### Step 4: API Service Setup

#### RapidAPI - YouTube Transcript
1. Sign up at https://rapidapi.com
2. Subscribe to "YouTube Transcript" API
3. Copy your API key
4. Add to environment variables as `RAPIDAPI_KEY`

#### Vizard AI
1. Sign up at https://vizard.ai
2. Go to Settings → API
3. Generate an API key
4. Add to environment variables as `VIZARD_API_KEY`

**Note**: Vizard AI API may require contacting their support for API access. Alternative: You can modify the workflow to use other video editing APIs like:
- Runway ML
- Descript API
- Pictory.ai API

### Step 5: Activate the Workflow

1. Open the imported workflow
2. Click on the "Webhook - Receive YouTube Link" node
3. Copy the webhook URL (it will be displayed in the node)
4. Click "Save" and then "Activate" the workflow

## Usage

### API Endpoint

Send a POST request to your webhook URL with this JSON payload:

```json
{
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "client_email": "client@example.com",
  "client_name": "John Doe"
}
```

### Example cURL Request

```bash
curl -X POST https://your-n8n-instance.com/webhook/youtube-automation \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "client_email": "client@example.com",
    "client_name": "John Doe"
  }'
```

### Supported YouTube URL Formats

The workflow supports all standard YouTube URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## Workflow Output

### Google Drive Folder Structure

```
YouTube_Content_VIDEO_ID_TIMESTAMP/
├── X_Twitter_Posts.txt
├── LinkedIn_Posts.txt
├── Instagram_Posts.txt
├── Content_Hooks.txt
└── Vizard_AI_Info.txt
```

### Email Notification

Clients receive a beautifully formatted HTML email containing:
- Summary of generated content
- Direct link to Google Drive folder
- List of all included assets
- Timestamp and source video link

## Customization Options

### Modify Post Generation

To customize the social media posts, edit the ChatGPT nodes:

**X Posts Node** (`ChatGPT - Create X Posts`):
- Adjust `temperature` (0.6-1.0) for creativity level
- Modify the system prompt for different tone/style
- Change `maxTokens` for longer/shorter posts

**LinkedIn Posts Node** (`ChatGPT - Create LinkedIn Posts`):
- Customize for your industry or niche
- Adjust formality level in system prompt

**Instagram Posts Node** (`ChatGPT - Create Instagram Posts`):
- Modify hashtag strategy
- Adjust emoji usage

### Change Number of Posts

In the prompt for each ChatGPT node, modify:
- "Create 3 X posts" → "Create 5 X posts"
- "Create 2 LinkedIn posts" → "Create 3 LinkedIn posts"

### Add Additional Platforms

To add TikTok, YouTube Shorts, or other platforms:

1. Duplicate a ChatGPT node
2. Rename it to your platform
3. Customize the system prompt
4. Add a corresponding Google Drive save node
5. Connect the nodes in the workflow

### Modify Vizard AI Settings

In the `Vizard AI - Create Shorts` node, you can adjust:
- `duration`: Video length (30, 60, 90 seconds)
- `style`: shorts, reels, tiktok
- `auto_caption`: true/false

## Troubleshooting

### Workflow Fails at Transcript Extraction

**Issue**: RapidAPI transcript extraction fails

**Solutions**:
1. Verify your RapidAPI key is correct
2. Check if video has captions/transcript available
3. Ensure your RapidAPI subscription is active
4. Try with a different YouTube video

### ChatGPT Responses Not Parsing

**Issue**: JSON parsing fails in "Parse Hooks Data" node

**Solution**: The node has fallback logic, but you can:
1. Adjust ChatGPT temperature (lower = more consistent)
2. Modify the prompt to be more explicit about JSON format
3. Check OpenAI API status

### Vizard AI Not Creating Videos

**Issue**: Vizard API returns errors

**Solutions**:
1. Verify API key is correct
2. Check Vizard API documentation for endpoint changes
3. Consider alternative video APIs (see setup section)
4. Contact Vizard support for API access

### Google Drive Permission Errors

**Issue**: Cannot create folder or save files

**Solutions**:
1. Re-authenticate Google Drive OAuth2
2. Ensure Drive API is enabled in Google Cloud Console
3. Check credential permissions include Drive file creation

### Email Not Sending

**Issue**: SMTP errors when sending email

**Solutions**:
1. Verify SMTP credentials
2. For Gmail: Enable "Less secure app access" or use App Password
3. Check firewall/network allows SMTP connections
4. Test SMTP settings with a simple test email

## Performance & Limits

### Expected Processing Time
- Transcript extraction: 5-15 seconds
- Hook identification: 10-20 seconds
- Social post generation: 15-30 seconds
- Vizard video creation: 2-5 minutes (async)
- Total workflow: ~1-2 minutes (video processing continues in background)

### API Rate Limits
- RapidAPI: Depends on your subscription tier
- OpenAI: 3,500 requests/minute (GPT-4)
- Vizard: Check your plan limits
- Google Drive: 1,000 requests per 100 seconds

### Cost Estimates (Per Execution)
- RapidAPI transcript: $0.001 - $0.01
- OpenAI GPT-4: $0.10 - $0.30 (4 calls)
- Vizard AI: Depends on plan
- Google Drive: Free
- Total: ~$0.15 - $0.50 per video

## Advanced Features

### Webhook Security

Add authentication to your webhook:

1. Edit the Webhook node
2. Enable "Authentication"
3. Choose "Header Auth" or "Basic Auth"
4. Set credentials

### Error Handling

The workflow includes basic error handling. To enhance:

1. Add "Error Trigger" nodes
2. Create alternative paths for failures
3. Send error notifications to admin email

### Batch Processing

To process multiple videos:

1. Modify webhook to accept array of URLs
2. Add "Split In Batches" node after webhook
3. Process each video through the workflow
4. Merge results before final email

### Analytics & Logging

Add tracking:

1. Insert HTTP Request nodes to log to analytics service
2. Track: processing time, success rate, API costs
3. Store metrics in database or Google Sheets

## Integration Examples

### Zapier Integration

Use the webhook URL in Zapier to trigger from:
- Google Sheets (new row with YouTube URL)
- Airtable
- Form submissions
- Slack commands

### Make.com Integration

Connect the workflow to Make.com scenarios for:
- CRM integration (HubSpot, Salesforce)
- Project management (Asana, Monday.com)
- Calendar scheduling

### Direct API Usage

Integrate into your own applications:

```javascript
// Node.js Example
const axios = require('axios');

async function processYouTubeVideo(videoUrl, clientEmail, clientName) {
  try {
    const response = await axios.post('YOUR_WEBHOOK_URL', {
      youtube_url: videoUrl,
      client_email: clientEmail,
      client_name: clientName
    });

    console.log('Success:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error:', error.response?.data || error.message);
    throw error;
  }
}

// Usage
processYouTubeVideo(
  'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
  'client@example.com',
  'John Doe'
);
```

## Security Best Practices

1. **API Keys**: Never commit API keys to git repositories
2. **Webhook URL**: Keep your webhook URL private or use authentication
3. **OAuth Tokens**: Regularly rotate Google OAuth tokens
4. **SMTP**: Use app-specific passwords, not main account password
5. **Environment Variables**: Use n8n's encrypted environment variables
6. **Access Control**: Limit Google Drive folder permissions

## Support & Resources

### Documentation Links
- [n8n Documentation](https://docs.n8n.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [RapidAPI YouTube Transcript](https://rapidapi.com/yashagarwal/api/youtube-transcript3)
- [Vizard AI](https://vizard.ai)
- [Google Drive API](https://developers.google.com/drive/api/v3/reference)

### Common Issues & Solutions
Check the GitHub issues page or n8n community forum for help.

## Changelog

### Version 1.0.0 (2025-11-06)
- Initial release
- Full automation pipeline
- Multi-platform social media post generation
- Vizard AI integration
- Google Drive storage
- Email notifications

## License

This workflow is provided as-is for educational and commercial use. Please ensure you comply with all API providers' terms of service.

## Credits

Built with:
- n8n - Workflow Automation
- OpenAI GPT-4 - Content Generation
- RapidAPI - Transcript Extraction
- Vizard AI - Video Processing
- Google Drive - Storage
- SMTP - Email Delivery
