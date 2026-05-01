# 🎧 Vibeify — AI-Powered Mood Music Recommender

🚀 AI-powered music recommendation system that interprets emotional intent and delivers personalized songs with dynamic video and album artwork integration.

**Live Demo:** https://vibeify.streamlit.app/

Vibeify analyzes natural language mood input and curates emotionally aligned music recommendations. Unlike traditional music apps that rely on genre or manual selection, it focuses on what the user _feels_, not just what they type.

## ✨ Features

- **🎭 Mood Detection:** AI identifies your emotional state from natural language input in any language
- **🧠 Intent-Aware Recommendations:** Understands what you emotionally NEED, not just what you said (anxious → calming songs)
- **🎧 DJ Mode:** Creates a 9-song progressive journey across 3 phases (Meet → Shift → Lift) that gently transitions your mood
- **🌍 Multilingual Support:** Accepts mood input in any language and recommends songs in your preferred languages
- **🎵 Real Album Artwork:** Fetches actual album covers from iTunes API for visual music discovery
- **▶️ YouTube Integration:** Direct play buttons that open the exact song on YouTube
- **🛡️ API Fallback Handling:** Gracefully handles quota limits using search fallback
- **❤️ Song Feedback:** Like/dislike system to express preferences
- **📊 Mood History:** Tracks your past mood searches in an elegant sidebar

## 🏗️ Architecture

                ┌──────────────────────┐
                │   User Interface     │
                │     (Streamlit)      │
                └─────────┬────────────┘
                          │
                          ▼
                ┌──────────────────────┐
                │   Application Logic  │
                │     (utility.py)     │
                │  - Mood Analysis     │
                │  - Recommendation    │
                │  - API Handling      │
                └───────┬──────────────┘
                        │
        ┌───────────────┼────────────────┐
        ▼                                ▼

┌───────────────┐ ┌──────────────────┐
│ Groq API │ │ YouTube API │
│ (LLaMA 3.3) │ │ (Video Search) │
│ - Mood Detect │ │ - Song Videos │
│ - Song Recs │ └──────────────────┘
└───────────────┘
│
▼
┌──────────────────┐
│ iTunes API │
│ - Album Artwork │
└──────────────────┘

**Data Flow:**

1. User describes their mood in natural language
2. Groq AI (LLaMA 3.3-70B) analyzes emotional state
3. AI generates personalized song recommendations
4. YouTube API fetches exact video links
5. iTunes API retrieves album artwork
6. Results rendered in premium UI with real-time feedback

## 🛠️ Tech Stack

- **Frontend:** Streamlit with custom CSS
- **AI/ML:** Groq API (LLaMA 3.3-70B-Versatile)
- **APIs:** YouTube Data API v3, iTunes Search API
- **Language:** Python 3.11+
- **Deployment:** Streamlit Cloud
- **Version Control:** Git & GitHub

## 📁 Project Structure

vibeify/
├── app.py # Main UI and application logic
├── utility.py # AI functions and API handlers
├── style.css # Premium dark theme styling
├── requirements.txt # Python dependencies
├── .env # API keys (local only, gitignored)
└── .gitignore # Git ignore rules

## 🚀 Local Setup

1. **Clone the repository:**

```bash
   git clone https://github.com/Utsahsinha9/Vibeify.git
   cd Vibeify
```

2. **Install dependencies:**

```bash
   pip install -r requirements.txt
```

3. **Set up API keys:**
   Create a `.env` file in the root directory:

GROQ_API_KEY=your_groq_api_key
YOUTUBE_API_KEY=your_youtube_api_key

4. **Run the app:**

```bash
   streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🧠 Key Learnings & Technical Decisions

**Why Groq over OpenAI/Gemini?**

- Free tier with generous limits
- LLaMA 3.3-70B offers excellent reasoning for mood analysis
- Fast response times (<2s) crucial for good UX

**Prompt Engineering Strategy:**

- Intent-aware prompting: "what this person emotionally NEEDS" vs "what they said"
- Strict output formatting with delimiters for reliable parsing
- Language enforcement to prevent model drift

**Session State Management:**

- Results stored in `st.session_state` to persist across button clicks
- Prevents playlist disappearing when user interacts with feedback buttons
- Critical for Streamlit's rerun architecture

**iTunes vs Spotify API:**

- iTunes API requires zero authentication and is completely free
- Returns high-quality 300x300 album artwork
- No rate limits for basic usage

## 🎯 Future Enhancements

- [ ] User authentication and persistent liked songs database
- [ ] Spotify OAuth integration for playlist export
- [ ] Audio analysis-based recommendations (tempo, key, energy)
- [ ] Collaborative filtering based on user feedback
- [ ] Weekly mood reports with data visualization

## 📄 License

This project is licensed under the MIT License.
