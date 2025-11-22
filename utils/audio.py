# [file name]: audio.py
import pyttsx3
import os
import threading
import re
import queue
import time


class AudioManager:
    def __init__(self):
        self.engine = None
        self.audio_queue = queue.Queue()
        self.is_playing = False
        self._initialize_engine()
        self._start_audio_worker()

    def _initialize_engine(self):
        """Initialize the TTS engine once."""
        try:
            self.engine = pyttsx3.init()

            # Improved voice settings
            voices = self.engine.getProperty('voices')
            if voices:
                # Prefer female voice if available
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break
                else:
                    self.engine.setProperty('voice', voices[0].id)

            # Optimized settings
            self.engine.setProperty('rate', 170)
            self.engine.setProperty('volume', 0.8)

        except Exception as e:
            print(f"Audio engine initialization failed: {e}")
            self.engine = None

    def _start_audio_worker(self):
        """Start a dedicated thread for audio playback."""

        def audio_worker():
            while True:
                try:
                    text = self.audio_queue.get(timeout=1)
                    if text is None:  # Shutdown signal
                        break

                    self.is_playing = True
                    try:
                        # Clean text for speech
                        clean_text = self._clean_text_for_speech(text)
                        if clean_text and self.engine:
                            self.engine.say(clean_text)
                            self.engine.runAndWait()
                    except Exception as e:
                        print(f"Audio playback error: {e}")
                    finally:
                        self.is_playing = False
                        self.audio_queue.task_done()

                except queue.Empty:
                    continue

        self.audio_thread = threading.Thread(target=audio_worker, daemon=True)
        self.audio_thread.start()

    def text_to_audio(self, text, auto_play=False):
        """
        Convert text to audio file and optionally queue for playback.
        Returns audio bytes for Streamlit.
        """
        if not text or not self.engine:
            return None

        output_file = "response_audio.mp3"

        try:
            # Clean text for better speech
            clean_text = self._clean_text_for_speech(text)

            # Queue for auto-play if requested
            if auto_play and clean_text:
                # Limit length for auto-play to avoid long speeches
                play_text = clean_text[:400]
                if not self.audio_queue.empty():
                    # Clear queue if there's pending audio to avoid backlog
                    try:
                        while not self.audio_queue.empty():
                            self.audio_queue.get_nowait()
                            self.audio_queue.task_done()
                    except queue.Empty:
                        pass

                self.audio_queue.put(play_text)

            # Save to file for Streamlit audio component (longer text)
            save_text = clean_text[:800] if clean_text else text[:800]
            self.engine.save_to_file(save_text, output_file)
            self.engine.runAndWait()

            # Read the file back as bytes for Streamlit
            if os.path.exists(output_file):
                with open(output_file, "rb") as f:
                    audio_bytes = f.read()
                return audio_bytes

        except Exception as e:
            print(f"Audio generation error: {e}")

        return None

    def _clean_text_for_speech(self, text):
        """Clean text for better TTS output."""
        if not text:
            return ""

        # Remove markdown headers
        cleaned = re.sub(r'#+\s*', '', text)
        # Remove URLs
        cleaned = re.sub(r'http[s]?://\S+', '', cleaned)
        # Remove special characters that might cause issues
        cleaned = re.sub(r'[*_~`]', '', cleaned)
        # Remove excessive newlines
        cleaned = re.sub(r'\n+', '. ', cleaned)
        # Limit consecutive spaces
        cleaned = re.sub(r'\s+', ' ', cleaned)

        return cleaned.strip()

    def stop_audio(self):
        """Stop any currently playing audio."""
        try:
            if self.engine:
                self.engine.stop()
            # Clear the queue
            while not self.audio_queue.empty():
                try:
                    self.audio_queue.get_nowait()
                    self.audio_queue.task_done()
                except queue.Empty:
                    break
            self.is_playing = False
        except Exception as e:
            print(f"Error stopping audio: {e}")

    def __del__(self):
        """Cleanup when object is destroyed."""
        self.stop_audio()


# Global instance - SINGLETON pattern to avoid multiple engines
_audio_manager = None


def get_audio_manager():
    """Get the singleton audio manager instance."""
    global _audio_manager
    if _audio_manager is None:
        _audio_manager = AudioManager()
    return _audio_manager


def text_to_audio(text, auto_play=True):
    """Wrapper function for backward compatibility."""
    manager = get_audio_manager()
    return manager.text_to_audio(text, auto_play=auto_play)


def stop_audio():
    """Stop any playing audio."""
    manager = get_audio_manager()
    manager.stop_audio()