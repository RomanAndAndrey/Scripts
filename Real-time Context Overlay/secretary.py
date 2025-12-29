import os
import queue
import threading

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class SecretaryAgent:
    def __init__(self, input_queue: queue.Queue, update_callback):
        self.input_queue = input_queue
        self.update_callback = update_callback  # Function to call with new bullets
        self.running = False
        self.buffer = []
        self.buffer_limit = 15  # Configurable

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("WARNING: GROQ_API_KEY not found in .env")

        self.client = Groq(api_key=api_key)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._process_loop, daemon=True)
        self.thread.start()
        print("Secretary Agent started.")

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join(timeout=1)

    def clear(self):
        self.buffer = []
        print("Secretary buffer cleared.")

    def _process_loop(self):
        while self.running:
            try:
                # Wait for text from listener
                text = self.input_queue.get(timeout=1)
                self.buffer.append(text)

                if len(self.buffer) >= self.buffer_limit:
                    self._generate_summary()
                    # Keep last few phrases for continuity?
                    # User said "Each 15-20 phrases send text...".
                    # Sending chunks is easier.
                    self.buffer = []  # Clear buffer after processing

            except queue.Empty:
                continue
            except Exception as e:
                print(f"Secretary Error: {e}")

    def _generate_summary(self):
        context = "\n".join(self.buffer)
        prompt = (
            "Твоя задача — выделить 3 главных смысловых буллета из текущего контекста разговора. "
            "Будь предельно краток. Отвечай только буллетами.\n\n"
            f"Разговор:\n{context}"
        )

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",  # Or mixr
            )

            content = chat_completion.choices[0].message.content
            print(f"Generated Summary:\n{content}")

            # Simple parsing of bullets if needed, or just pass raw text if formatted well
            bullets = [line.strip() for line in content.split("\n") if line.strip()]
            # Filter to keep typically 3 lines
            # bullets = bullets[:3]

            self.update_callback(bullets)

        except Exception as e:
            print(f"LLM Error: {e}")
