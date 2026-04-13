"""
Miss Pretty Kitty - Main Loop (Text Test Mode)
Stripped down version for testing brain only
"""

import time
import signal
import sys
from mpk_llm import MissPrettyKitty


class MissPrettyKittyApp:
    def __init__(self):
        print("\n✨ Booting Miss Pretty Kitty... ✨\n")
        self.brain = MissPrettyKitty()
        self.running = True
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)
        print("\n🐱 Miss Pretty Kitty is ALIVE!\n")

    def _shutdown(self, *args):
        print("\n\n💕 Miss Pretty Kitty is going to sleep~ byebye!")
        self.running = False
        sys.exit(0)

    def run_text_mode(self):
        print("⌨️  Text mode — type to Miss Pretty Kitty!")
        print("   'clear' to reset memory | 'quit' to exit\n")
        while self.running:
            try:
                text = input("You: ").strip()
                if not text:
                    continue
                if text.lower() in ["quit", "exit", "bye"]:
                    self._shutdown()
                if text.lower() == "clear":
                    self.brain.clear_memory()
                    continue
                print("\nMiss Pretty Kitty: ", end="", flush=True)
                response = self.brain.chat(text)
                print(f"{response}\n")
            except EOFError:
                self._shutdown()


if __name__ == "__main__":
    app = MissPrettyKittyApp()
    app.run_text_mode()
