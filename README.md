# YouTube Content Automation Workflow

Automate your YouTube content repurposing with this powerful n8n workflow. Transform any YouTube video into engaging social media posts for X (Twitter), LinkedIn, and Instagram, plus AI-generated short videos, all delivered to your clients via Google Drive.

## 🎯 What This Does

1. **Receives** YouTube video links via webhook
2. **Extracts** video transcripts using RapidAPI
3. **Identifies** engaging content hooks using ChatGPT
4. **Generates** platform-specific social media posts:
   - 3x X (Twitter) posts
   - 2x LinkedIn posts
   - 2x Instagram captions with hashtags
5. **Creates** short-form videos using Vizard AI
6. **Saves** everything to Google Drive in organized folders
7. **Emails** clients with the Google Drive link

## 🚀 Quick Start

### 1. Import the Workflow

1. Open your n8n instance
2. Go to **Workflows** → **Import from File**
3. Select `youtube-content-automation-workflow.json`

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your keys:

```bash
RAPIDAPI_KEY=your_rapidapi_key
VIZARD_API_KEY=your_vizard_key
SENDER_EMAIL=your_email@domain.com
```

### 3. Set Up Credentials in n8n

Configure these in **Settings** → **Credentials**:

- ✅ OpenAI API
- ✅ Google Drive OAuth2
- ✅ SMTP Email

### 4. Activate Workflow

Click **Save** then **Activate** in n8n.

## 📡 Usage

Send a POST request to your webhook URL:

```bash
curl -X POST https://your-n8n-instance.com/webhook/youtube-automation \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "client_email": "client@example.com",
    "client_name": "John Doe"
  }'
```

## 📁 Output

Your clients receive:
- **Google Drive folder** with all content
- **Beautiful HTML email** with direct link
- **Organized files**:
  - X (Twitter) posts
  - LinkedIn posts
  - Instagram captions
  - Content hooks analysis
  - Vizard AI video info

## 🛠️ Requirements

### API Services

- [RapidAPI](https://rapidapi.com) - YouTube Transcript API
- [OpenAI](https://platform.openai.com) - GPT-4 API
- [Vizard AI](https://vizard.ai) - Video shorts generation
- [Google Drive](https://drive.google.com) - Storage
- SMTP Email Account (Gmail, Outlook, etc.)

### Cost Estimate

Approximately **$0.15-$0.50 per video** processed:
- RapidAPI: ~$0.01
- OpenAI GPT-4: ~$0.10-$0.30
- Vizard AI: Varies by plan
- Google Drive: Free
- Email: Free

## 📖 Documentation

For detailed setup instructions, troubleshooting, and customization options, see [WORKFLOW_DOCUMENTATION.md](./WORKFLOW_DOCUMENTATION.md).

## 🔧 Customization

### Modify Number of Posts

Edit the ChatGPT node prompts:
- Change "Create 3 X posts" to your desired number
- Adjust `maxTokens` for longer/shorter content

### Add New Platforms

1. Duplicate a ChatGPT node
2. Customize the prompt for your platform
3. Add a Google Drive save node
4. Connect in the workflow

### Change AI Model

In ChatGPT nodes, update `modelId`:
- `gpt-4-turbo-preview` (current)
- `gpt-4`
- `gpt-3.5-turbo` (cheaper, faster)

## 🐛 Troubleshooting

### Transcript Extraction Fails
- Verify RapidAPI key and subscription
- Ensure video has captions available
- Try a different YouTube video

### Email Not Sending
- Check SMTP credentials
- Use app-specific password for Gmail
- Verify firewall allows SMTP

### Google Drive Errors
- Re-authenticate OAuth2
- Check Drive API is enabled
- Verify folder permissions

See [WORKFLOW_DOCUMENTATION.md](./WORKFLOW_DOCUMENTATION.md) for more solutions.

## 🔐 Security

- ✅ Never commit `.env` file
- ✅ Use app-specific passwords
- ✅ Rotate API keys regularly
- ✅ Enable webhook authentication
- ✅ Use encrypted environment variables

## 📊 Workflow Nodes

The workflow includes 19 nodes:

1. Webhook Trigger
2. Video ID Extractor
3. RapidAPI Transcript
4. ChatGPT Hook Identifier
5. Hooks Parser
6. ChatGPT X Posts (3x)
7. ChatGPT LinkedIn Posts (2x)
8. ChatGPT Instagram Posts (2x)
9. Vizard AI Shorts Creator
10. Content Aggregator
11. Google Drive Folder Creator
12. Google Drive File Savers (5x)
13. Email Composer
14. Email Sender
15. Webhook Response

## 🤝 Integration Examples

### Zapier
Trigger from Google Sheets, forms, or CRM events

### Make.com
Connect to project management tools

### Custom API
Integrate into your own applications

```javascript
const response = await fetch('YOUR_WEBHOOK_URL', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    youtube_url: 'https://www.youtube.com/watch?v=VIDEO_ID',
    client_email: 'client@example.com',
    client_name: 'John Doe'
  })
});
```

## 📝 Example Output

### X (Twitter) Post
```
🚀 Just discovered this game-changing insight from @creator:

"[Hook quote from video]"

This completely changed how I think about [topic].

Watch the full video: [link]

#ContentCreation #Marketing #YouTubeTips
```

### LinkedIn Post
```
I recently watched an insightful video about [topic], and one point really stood out:

[Hook with context and professional framing]

This insight is particularly relevant for [industry/professionals] because...

[Call to action]

What are your thoughts on this approach?

#ProfessionalDevelopment #Industry #Insights
```

### Instagram Caption
```
💡 Mind-blown by this insight!

[Engaging hook with emojis and line breaks]

Swipe to see more →

#contentcreator #socialmedia #marketing #digitalmarketing #contentstrategy #smallbusiness #entrepreneur #marketingtips #growyourbusiness #socialmediatips
```

## 🌟 Features

- ✅ Fully automated workflow
- ✅ Multi-platform content generation
- ✅ AI-powered hook identification
- ✅ Professional email templates
- ✅ Organized Google Drive storage
- ✅ Error handling and fallbacks
- ✅ Webhook API for easy integration
- ✅ Customizable prompts and outputs
- ✅ Scalable architecture
- ✅ Cost-effective processing

## 📦 Files Included

```
.
├── youtube-content-automation-workflow.json  # n8n workflow file
├── WORKFLOW_DOCUMENTATION.md                 # Detailed documentation
├── .env.example                              # Environment variables template
├── README.md                                 # This file
├── app.py                                    # Existing Flask app
├── requirements.txt                          # Python dependencies
└── Procfile                                  # Heroku configuration
```

## 🔄 Workflow Process

```
YouTube URL → Extract Transcript → Identify Hooks → Generate Posts
                                         ↓
                                    Create Shorts
                                         ↓
                Save to Google Drive → Email Client → Done!
```

## 💡 Use Cases

- **Content Agencies**: Scale client deliverables
- **Social Media Managers**: Repurpose video content
- **YouTubers**: Promote videos across platforms
- **Marketers**: Multi-channel content distribution
- **Freelancers**: Automate client work

## 🎓 Learning Resources

- [n8n Documentation](https://docs.n8n.io/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [Content Marketing Guide](https://contentmarketinginstitute.com/)

## 📞 Support

For issues or questions:
1. Check [WORKFLOW_DOCUMENTATION.md](./WORKFLOW_DOCUMENTATION.md)
2. Review n8n community forum
3. Check API provider documentation

## 📜 License

MIT License - Free to use and modify

## 🙏 Credits

Built with powerful automation tools:
- **n8n** - Workflow automation
- **OpenAI GPT-4** - AI content generation
- **RapidAPI** - Transcript extraction
- **Vizard AI** - Video processing
- **Google Drive** - Cloud storage

---

**Ready to automate your content workflow? Import the workflow and start transforming YouTube videos into engaging social media content!** 🚀
