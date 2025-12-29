import io
import os
import queue
import threading
import time

import numpy as np
import sounddevice as sd
import soundfile as sf
import torch
import whisper


class ListenerAgent:
    def __init__(self, output_queue: queue.Queue, model_size="small"):
        self.output_queue = output_queue
        self.running = False
        self.fs = 16000  # Sample rate for Whisper
        self.channels = 1

        # VAD Parameters
        self.threshold = 0.02  # Adjust sensitivity
        self.silence_duration = 1.0  # Seconds of silence to mark end of phrase
        self.min_phrase_len = 0.5  # Minimum phrase length

        print(f"Loading Whisper model '{model_size}'...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(model_size, device=device)
        print(f"Model loaded on {device}.")

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        print("Listener Agent started (SoundDevice).")

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1)

    def _listen_loop(self):
        # Buffer to hold current phrase audio
        phrase_buffer = []
        silence_start = None
        is_speaking = False

        def callback(indata, frames, time, status):
            if status:
                print(status)
            # Add to temporary queue or process here?
            # Processing in callback is bad. Use a queue or handling logic in main loop?
            # But sd.InputStream with callback is efficient.
            # Let's use a stream queue to move data to _process loop?
            # actually, let's keep it simple: blocking read in loop.
            pass

        # Using blocking read for simplicity in a thread
        with sd.InputStream(samplerate=self.fs, channels=self.channels, callback=None) as stream:
            while self.running:
                # Read chunks of 200ms
                chunk_duration = 0.2
                frames_to_read = int(self.fs * chunk_duration)
                data, overflow = stream.read(frames_to_read)

                # Check volume
                rms = np.sqrt(np.mean(data**2))

                if rms > self.threshold:
                    if not is_speaking:
                        is_speaking = True
                        print("Speaking started...")
                        phrase_buffer = []  # Start fresh

                    silence_start = None
                    phrase_buffer.append(data)

                elif is_speaking:
                    # Currently speaking but quiet chunk
                    phrase_buffer.append(data)

                    if silence_start is None:
                        silence_start = time.time()
                    else:
                        if time.time() - silence_start > self.silence_duration:
                            # Phrase ended
                            print("Phrase ended.")
                            is_speaking = False

                            # Concatenate and transcribe
                            full_audio = np.concatenate(phrase_buffer, axis=0)
                            duration = len(full_audio) / self.fs

                            if duration >= self.min_phrase_len:
                                self._transcribe(full_audio)

                            phrase_buffer = []
                            silence_start = None

    def _transcribe(self, audio_data):
        try:
            # Flatten audio_data if needed
            audio_data = audio_data.flatten()

            # Whisper expects float32 array, sounddevice returns float32 by default

            # Transcribe directly
            # whisper.transcribe accepts numpy array
            result = self.model.transcribe(
                audio_data, fp16=torch.cuda.is_available(), language="ru"
            )
            text = result.get("text", "").strip()

            if text:
                print(f"Heard: {text}")
                self.output_queue.put(text)

        except Exception as e:
            print(f"Transcription Error: {e}")
