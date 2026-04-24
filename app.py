import streamlit as st
from utils import get_mood_category, get_recommendations, get_dj_playlist

st.set_page_config(
    page_title = "Vibeify",
    page_icon="🎵",
    layout="centered"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)")

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

with st.sidebar:
    st.markdown("### 🕘 Mood History")

    if len(st.session_state.mood_history) == 0 :
        st.markdown("*Your mood history will appear here..*")
    else:
        for item in st.session_state.mood_history:
            st.markdown(f"""
                <div class="history-item">
                    🎭 <b>{item['mood_label']}</b><br>
                    <small>{item['mood_input']}</small>
                </div>
            """, unsafe_allow_html=True)
        
        # Button to clear history
        if st.button("🗑️ Clear History"):
            st.session_state.mood_history = []
            st.rerun()      
