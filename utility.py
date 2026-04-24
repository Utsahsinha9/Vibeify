from dotenv import load_dotenv
load_dotenv()
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def get_mood_category(mood):
    """
    Takes the user's raw mood text
    Returns a short mood label like 'Anxious' or 'Happy & Energetic'
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
                The user says they are feeling: {mood}
                
                Identify their emotional state in 3 words or less.
                Examples: Anxious, Happy & Energetic, Sad & Lonely, Restless, Calm
                
                Reply with ONLY the mood label. Nothing else.
                """
            }
        ]
    )
    return response.choices[0].message.content.strip()


def get_recommendations(mood, language):
    """
    Takes mood and language preference
    Returns a list of 5 song dictionaries
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
                The user is feeling: {mood}
                Preferred language: {language}

                Think about what this person emotionally NEEDS right now, not just what they said.
                For example: if someone feels anxious or restless, they need calming soothing songs.
                If someone feels sad, recommend songs that comfort and validate their feelings.
                If someone feels happy, recommend upbeat celebratory songs.

                Recommend exactly 5 songs matching this emotional need and language preference.

                Respond in this EXACT format, nothing else:
                1. [Song Name] | [Artist Name] | [One sentence why it matches]
                2. [Song Name] | [Artist Name] | [One sentence why it matches]
                3. [Song Name] | [Artist Name] | [One sentence why it matches]
                4. [Song Name] | [Artist Name] | [One sentence why it matches]
                5. [Song Name] | [Artist Name] | [One sentence why it matches]
                """
            }
        ]
    )

    raw = response.choices[0].message.content.strip()

    songs = []
    for line in raw.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            parts = line.split("|")
            if len(parts) == 3:
                songs.append({
                    "name": parts[0].split(".", 1)[1].strip(),
                    "artist": parts[1].strip(),
                    "reason": parts[2].strip()
                })
    return songs


def get_dj_playlist(mood, language):
    """
    Takes mood and language
    Returns a progressive playlist across 3 phases
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
                The user is currently feeling: {mood}
                Preferred language: {language}

                Act as a professional DJ who reads the room.
                Create a 9-song progressive playlist in 3 phases:

                PHASE 1 - MEET (3 songs): Songs that match and validate
                the user's current emotion exactly.

                PHASE 2 - SHIFT (3 songs): Songs that gently transition
                the mood — not too different but slightly more positive.

                PHASE 3 - LIFT (3 songs): Songs that bring the user to
                an uplifted, positive, energetic feeling.

                Respond in this EXACT format:
                PHASE1:
                1. [Song] | [Artist] | [Why it matches current mood]
                2. [Song] | [Artist] | [Why it matches current mood]
                3. [Song] | [Artist] | [Why it matches current mood]
                PHASE2:
                1. [Song] | [Artist] | [Why it transitions]
                2. [Song] | [Artist] | [Why it transitions]
                3. [Song] | [Artist] | [Why it transitions]
                PHASE3:
                1. [Song] | [Artist] | [Why it lifts]
                2. [Song] | [Artist] | [Why it lifts]
                3. [Song] | [Artist] | [Why it lifts]
                """
            }
        ]
    )

    raw = response.choices[0].message.content.strip()

    playlist = {
        "phase1": {"label": "🎭 Phase 1 — Meet (where you are)", "songs": []},
        "phase2": {"label": "🌅 Phase 2 — Shift (gentle transition)", "songs": []},
        "phase3": {"label": "🚀 Phase 3 — Lift (feeling better)", "songs": []}
    }

    current_phase = None

    for line in raw.split("\n"):
        line = line.strip()

        if line.startswith("PHASE1:"):
            current_phase = "phase1"
        elif line.startswith("PHASE2:"):
            current_phase = "phase2"
        elif line.startswith("PHASE3:"):
            current_phase = "phase3"
        elif current_phase and line and line[0].isdigit():
            parts = line.split("|")
            if len(parts) == 3:
                playlist[current_phase]["songs"].append({
                    "name": parts[0].split(".", 1)[1].strip(),
                    "artist": parts[1].strip(),
                    "reason": parts[2].strip()
                })

    return playlist