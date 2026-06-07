import time
import base64
import streamlit as st


class VoicePipeline:
    def __init__(self, llm, tts):
        self.llm = llm
        self.tts = tts
        self.last_spoken_at = 0

    def _find_form_issue(self, exercise, metrics):
        if not metrics:
            return None

        if "issue" in metrics:
            return metrics["issue"]

        return None

    def process_event(self, event, exercise, metrics):
        try:

            issue = self._find_form_issue(exercise, metrics)

            now = time.time()

            is_major_event = event in [
                "workout_started",
                "set_completed",
                "workout_completed"
            ]

            if not is_major_event:
                if not issue:
                    print("No issue found")
                    return None

                if now - self.last_spoken_at < 5:
                    print("Cooldown active")
                    return None


            text = self.llm.give_feedback(event, issue)


            if not text:
                print("No feedback generated")
                return None

            voice = self.tts.speak(text)

            self.last_spoken_at = now

            return voice, text

        except Exception as e:
            print("VOICE PIPELINE ERROR:", repr(e))
            raise


def autoplay_audio(audio_bytes):
    if not audio_bytes:
        return

    b64 = base64.b64encode(audio_bytes).decode()

    st.markdown(
        f"""
        <audio autoplay style="display:none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True,
    )