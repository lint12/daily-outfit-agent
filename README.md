# 👔 Daily Outfit Agent

Your personal AI stylist powered by MCP (Model Context Protocol)!

## What Is This?

An intelligent outfit recommendation system that creates **personalized outfit suggestions** just for you, based on:
- 🌸 **Current season** - Weather-appropriate pieces
- 🎨 **Your style profile** - Colors, preferences, body type from `style_interests.md`
- 👗 **Reddit fashion trends** - Real outfit inspiration from fashion communities
- 🤖 **AI styling** - Custom outfit recommendations with styling tips
- 📧 **Email delivery** - Automatic delivery to your inbox

## ✨ Features

- ✅ **Personalized outfit creation** - AI generates complete outfits tailored to you
- ✅ **Season-aware recommendations** - Appropriate for current weather
- ✅ **Gender & body type conscious** - Respects your preferences and fit needs
- ✅ **Reddit-inspired** - Gets real-world outfit ideas from fashion subreddits
- ✅ **Automatic email delivery** - Beautiful HTML emails with your daily outfit
- ✅ **Simple MCP architecture** - Clean server/client design with Jupyter notebook
- ✅ **Easy to customize** - Just edit your `style_interests.md` file

## 🚀 Quick Start

### 1. Set Up Your Style Profile
```bash
# Edit your style preferences
open src/server/data/style_interests.md
```

Add your gender, favorite colors, style preferences, body type, and favorite subreddits.

### 2. Configure Email (Optional but Recommended)
Create a `.env` file in the project root:
```bash
# For Gmail (recommended):
MCP_SMTP_FROM_EMAIL=your.email@gmail.com
MCP_SMTP_PASSWORD=your-app-password  # See Gmail App Password setup below
```

**Gmail App Password Setup:**
1. Go to Google Account → Security → 2-Step Verification (enable if not already)
2. Go to App Passwords: https://myaccount.google.com/apppasswords
3. Create new app password, copy it to `.env` file

### 3. Start the Server
```bash
cd notebooks
jupyter notebook outfit_server.ipynb
```
Run cells in order:
- **Cell 1:** Imports
- **Cell 2:** Initialize services (including email)
- **Cell 3:** Define MCP tools
- **Cell 5:** Define MCP prompt
- **Cell 6:** Start server on port 8081

### 4. Run the Client
```bash
cd client
uv run outfit_client.py
```

The AI will automatically:
1. Check current season
2. Get your style profile and Reddit inspiration
3. Create a personalized outfit recommendation
4. Email it to you!

## 📂 Project Structure

```
daily-outfit-agent/
├── notebooks/
│   └── outfit_server.ipynb          # 🌟 MCP Server (run this!)
│
├── client/
│   ├── outfit_client.py             # FastAgent client
│   ├── fastagent.config.yaml        # Server configuration
│   └── pyproject.toml               # Client dependencies
│
├── src/server/
│   ├── services/
│   │   ├── reddit_service.py        # Fetch outfit posts from Reddit
│   │   ├── style_interests_service.py  # Parse style preferences
│   │   ├── season_service.py        # Season detection & keywords
│   │   └── email_service.py         # Email sending (SMTP/HTML)
│   ├── data/
│   │   └── style_interests.md       # 🎨 YOUR STYLE PREFERENCES
│   └── config/
│       ├── settings.py              # Server configuration
│       └── constants.py             # Constants
│
├── .env                             # Email credentials (create this)
└── README.md                        # This file
```

## 🛠️ MCP Tools Available

The server provides **3 essential tools**:

### 1. `get_season_info()`
Get current season and relevant fashion keywords.
```python
# Returns: season name + keywords like "layer", "coat", "sweater", etc.
```

### 2. `create_personalized_outfit(occasion="casual", limit_per_subreddit=5)`
Gather context to create a personalized outfit:
- Your style profile (gender, colors, preferences, body type)
- Current season keywords
- Reddit outfit inspiration from your favorite subreddits
```python
# Returns: Context string for AI to analyze and create outfit
```

### 3. `email_outfit_recommendation(outfit_recommendation, subject="")`
Email the AI-generated outfit to you with beautiful HTML formatting.
```python
# Sends: Complete outfit recommendation with styling tips
```

## 🎯 How It Works

### Workflow:
1. **Client asks** for outfit inspiration (via `daily_outfit_inspiration` prompt)
2. **Server detects season** and gathers your style profile
3. **Fetches Reddit posts** from your favorite fashion subreddits
4. **AI analyzes** the context and creates a specific outfit for YOU
5. **Generates recommendation** with:
   - 4-6 specific clothing items (not generic - actual pieces!)
   - Why it works for your style and body type
   - Styling tips
   - Where to shop
   - Alternative pieces
6. **Emails automatically** - Beautiful HTML email delivered to your inbox

### Example Output:
```
Complete Outfit:
• Black oversized turtleneck sweater
• High-waisted olive green wide-leg trousers
• White leather sneakers
• Beige wool coat
• Black leather tote bag

Why It Works:
This outfit combines your love for minimalist style with earth tones...

Styling Tips:
1. Tuck the front of the turtleneck for a relaxed look
2. Roll sleeves slightly for a casual vibe
3. Add gold jewelry for warmth

Where to Shop:
• Everlane - minimalist basics
• COS - modern tailoring
• Mango - affordable trendy pieces
```

## 🔧 Customization

### Style Interests File
Edit `src/server/data/style_interests.md` to include:
- **Personal Info:** Gender, style identity
- **Style Preferences:** Your fashion styles
- **Favorite Colors:** Colors you love
- **Favorite Subreddits:** Where to get inspiration
- **Occasion Types:** What you dress for
- **Body Type & Fit:** What fits you well
- **Notes:** Size, additional preferences

### Email Service
The email service (`src/server/services/email_service.py`) supports:
- Gmail (recommended) - use App Password
- Any SMTP server
- Beautiful HTML templates with CSS styling
- Automatic text fallback

## 📦 Dependencies

### Server (Jupyter)
- `fastmcp` - MCP server framework
- `praw` - Reddit API wrapper
- `pydantic` & `pydantic-settings` - Configuration
- `python-dotenv` - Environment variables
- `nest_asyncio` - Async in Jupyter

### Client
- `fast-agent-mcp` - MCP client framework
- `anthropic` - Claude API (for AI styling)

## 🤝 Contributing

This is a personal project but feel free to fork and customize for your own style needs!

## 📝 Notes

- **Reddit API:** Uses public Reddit (no auth required)
- **Privacy:** Your style preferences stay local in `style_interests.md`
- **Email:** Only sends to your own email (configured in `.env`)
- **AI Provider:** Uses Claude via Anthropic API (configured in `fastagent.config.yaml`)

## 🎨 Built With

- **FastMCP** - MCP server framework
- **FastAgent** - MCP client framework  
- **Reddit API** - Fashion inspiration source
- **SMTP** - Email delivery
- **Jupyter Notebook** - Interactive server development

---

*Get dressed with confidence every day! 👔✨*
