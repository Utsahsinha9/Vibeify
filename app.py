import streamlit as st
from utility import get_mood_category, get_recommendations, get_dj_playlist, get_youtube_url, get_album_art



# ===== PAGE CONFIG — must be first Streamlit command =====
st.set_page_config(
    page_title="Vibeify",
    page_icon="🎵",
    layout= "wide",
    initial_sidebar_state="expanded"

)

# ===== LOAD CSS =====
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===== SESSION STATE INITIALIZATION =====
# These are like memory slots that survive page reruns
if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

if "feedback" not in st.session_state:
    st.session_state.feedback = {}

if "last_songs" not in st.session_state:
    st.session_state.last_songs = []

if "last_mood_label" not in st.session_state:
    st.session_state.last_mood_label = ""

if "last_playlist" not in st.session_state:
    st.session_state.last_playlist = {}

if "last_mode" not in st.session_state:
    st.session_state.last_mode = ""

# ===== SIDEBAR — MOOD HISTORY =====
with st.sidebar:
    st.markdown("### 🕘 Mood History")

    if len(st.session_state.mood_history) == 0:
        st.markdown("*Your mood history will appear here after your first search...*")
    else:
        for item in reversed(st.session_state.mood_history):
            st.markdown(f"""
                <div class="history-item">
                    🎭 <b>{item['mood_label']}</b><br>
                    <small>{item['mood_input']}</small>
                </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ Clear History"):
            st.session_state.mood_history = []
            st.rerun()

# ===== HEADER =====
#st.markdown('<div class="title">🎵 Vibeify</div>', unsafe_allow_html=True)
st.markdown("""
<div class="title">
    <span class="logo-icon">
        <svg width="42" height="42" viewBox="0 0 24 24" fill="none" stroke="#F5A623" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 18V5l12-2v13"></path>
            <circle cx="6" cy="18" r="3"></circle>
            <circle cx="18" cy="16" r="3"></circle>
        </svg>
    </span>
    <span class="title-text">Vibeify</span>
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="subtitle">Tell me how you feel — I\'ll find the perfect songs for you</div>', unsafe_allow_html=True)
st.markdown("---")

# ===== LANGUAGE SELECTOR =====
st.markdown("**🌍 Select your preferred language(s):**")
languages = st.multiselect(
    "Pick from popular ones or add your own below",
    ["English", "Hindi", "Spanish", "K-Pop", "French", "Punjabi", "Tamil", "Arabic", "Portuguese", "Japanese", "Urdu", "Bengali"],
    default=["English"]
)

custom_language = st.text_input("🌐 Want songs in another language? Type it here:", placeholder="e.g. Swahili, Marathi, Gujarati...")

all_languages = languages.copy()
if custom_language.strip():
    all_languages.append(custom_language.strip())

language_str = ", ".join(all_languages) if all_languages else "English"

# ===== MOOD INPUT =====
st.markdown("**💭 How are you feeling right now?**")
mood = st.text_area(
    "Mood Input",
    placeholder="Type in any language! e.g. 'I had a breakup' or 'मैं थोड़ा उदास हूं' or 'Estoy feliz'",
    height=120
)

# ===== BUTTONS =====
col1, col2 = st.columns(2)
with col1:
    recommend_clicked = st.button("🎶 Get Recommendations", use_container_width=True)
with col2:
    dj_clicked = st.button("🎧 DJ Mode", use_container_width=True)

# ===== HANDLE RECOMMEND BUTTON =====
if recommend_clicked:
    if mood.strip() == "":
        st.warning("⚠️ Please describe your mood first!")
    else:
        with st.spinner("Finding the perfect songs for you..."):
            mood_label = get_mood_category(mood)
            try:
                songs = get_recommendations(mood, language_str)
            except Exception:
                st.error("⚠️ Something went wrong. Please try again.")
                songs = []

            # Store results in session state so they persist after button clicks
            st.session_state.last_songs = songs
            st.session_state.last_mood_label = mood_label
            st.session_state.last_mode = "recommend"

            # Save to mood history
            st.session_state.mood_history.append({
                "mood_label": mood_label,
                "mood_input": mood[:50] + "..." if len(mood) > 50 else mood
            })

# ===== HANDLE DJ MODE BUTTON =====
if dj_clicked:
    if mood.strip() == "":
        st.warning("⚠️ Please describe your mood first!")
    else:
        with st.spinner("Your DJ is reading the room..."):
            mood_label = get_mood_category(mood)
            try:
                playlist = get_dj_playlist(mood, language_str)
            except Exception:
                st.error("⚠️ DJ couldn't load. Try again.")
                playlist = {}

            # Store in session state
            st.session_state.last_playlist = playlist
            st.session_state.last_mood_label = mood_label
            st.session_state.last_mode = "dj"

            # Save to mood history
            st.session_state.mood_history.append({
                "mood_label": f"🎧 DJ: {mood_label}",
                "mood_input": mood[:50] + "..." if len(mood) > 50 else mood
            })

# ===== DISPLAY RECOMMEND RESULTS =====
if st.session_state.last_mode == "recommend" and st.session_state.last_songs:

    col_s1, col_s2 = st.columns([1, 5])
    with col_s1:
        if st.button("🔀 Shuffle"):
            import random
            random.shuffle(st.session_state.last_songs)
            st.rerun()
    

    st.markdown(f"""
        <div class="mood-badge">🎭 Detected Mood: {st.session_state.last_mood_label}</div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎵 Your Playlist")

    for i, song in enumerate(st.session_state.last_songs):
        song_key = f"rec_{song['name']}_{i}"
        youtube_url = get_youtube_url(song['name'], song['artist'])
        artwork = get_album_art(song['name'], song['artist'])  # ← NEW

        art_html = f'<img src="{artwork}" class="album-art">' if artwork else '<div class="album-art-placeholder">🎵</div>'

        st.markdown(f"""
            <div class="song-card">
                {art_html}
                <div class="song-info-premium">
                    <div class="song-title-premium">{song['name']}</div>
                    <div class="song-artist">{song['artist']}</div>
                    <div class="song-reason">{song['reason']}</div>
                    <a href="{youtube_url}" target="_blank" class="play-btn">▶ Play on YouTube</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Feedback buttons
        col_a, col_b, col_c = st.columns([1, 1, 8])
        with col_a:
            if st.button("👍", key=f"up_{song_key}"):
                st.session_state.feedback[song_key] = "liked"
        with col_b:
            if st.button("👎", key=f"down_{song_key}"):
                st.session_state.feedback[song_key] = "disliked"

        # Show feedback status
        if song_key in st.session_state.feedback:
            if st.session_state.feedback[song_key] == "liked":
                st.markdown("❤️ *Liked*")
            else:
                st.markdown("👎 *Disliked*")

        st.markdown("")

# ===== DISPLAY DJ MODE RESULTS =====
if st.session_state.last_mode == "dj" and st.session_state.last_playlist:

    st.markdown(f"""
        <div class="mood-badge">🎧 DJ Mode: {st.session_state.last_mood_label}</div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎧 Your DJ Playlist")
    st.markdown("*A musical journey crafted just for you*")

    for phase_key, phase_data in st.session_state.last_playlist.items():
        st.markdown(f"#### {phase_data['label']}")

        for i, song in enumerate(phase_data["songs"]):
            song_key = f"dj_{phase_key}_{i}"
            youtube_url = get_youtube_url(song['name'], song['artist'])
            artwork = get_album_art(song['name'], song['artist'])  # ← NEW

            art_html = f'<img src="{artwork}" class="album-art">' if artwork else '<div class="album-art-placeholder">🎵</div>'

            st.markdown(f"""
                <div class="dj-card">
                    {art_html}
                    <div class="song-info-premium">
                        <div class="song-title-premium">{song['name']}</div>
                        <div class="song-artist">{song['artist']}</div>
                        <div class="song-reason">{song['reason']}</div>
                        <a href="{youtube_url}" target="_blank" class="play-btn">▶ Play on YouTube</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # Feedback buttons
            col_a, col_b, col_c = st.columns([1, 1, 8])
            with col_a:
                if st.button("👍", key=f"up_{song_key}"):
                    st.session_state.feedback[song_key] = "liked"
            with col_b:
                if st.button("👎", key=f"down_{song_key}"):
                    st.session_state.feedback[song_key] = "disliked"

            if song_key in st.session_state.feedback:
                if st.session_state.feedback[song_key] == "liked":
                    st.markdown("❤️ *Liked*")
                else:
                    st.markdown("👎 *Disliked*")

            st.markdown("")

        st.markdown("---")