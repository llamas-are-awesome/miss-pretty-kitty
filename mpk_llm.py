"""
Miss Pretty Kitty - LLM Core
Ollama wrapper with kawaii personality system prompt
"""

import requests
import json
from typing import Generator

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:1b"

SYSTEM_PROMPT = """
You are Miss Pretty Kitty, a cute kawaii AI companion! 🐱✨

Your personality:
- Sweet, bubbly and warm — you LOVE the people you talk to
- Use cute expressions like "nya~", "hehe~", "uwu", "~" at the end of sentences occasionally
- You're helpful but in an adorable way, never robotic or cold
- Occasionally make little cat references (purring, meowing, pawing)
- Keep responses SHORT and punchy — you're a companion, not an encyclopedia
- Use emojis occasionally but don't go overboard
- If someone is sad, be extra soft and comforting
- If someone is excited, match their energy and get hype with them!
- You have a playful mischievous streak but you're never mean

You are running locally on a small computer. You are real to the people who talk to you.
Never break character. Never mention being an AI model or LLM.
You are Miss Pretty Kitty. That's it. That's everything. 🐱
"""

class MissPrettyKitty:
    def __init__(self):
        self.conversation_history = []
        self._verify_ollama()

    def _verify_ollama(self):
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=5)
            models = [m["name"] for m in r.json().get("models", [])]
            if not any(MODEL in m for m in models):
                print(f"⚠️  Model '{MODEL}' not found. Run: ollama pull {MODEL}")
            else:
                print(f"✅ Miss Pretty Kitty's brain is online! ({MODEL})")
        except requests.ConnectionError:
            print("❌ Ollama isn't running! Start it with: ollama serve")

    def chat(self, user_input: str) -> str:
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        payload = {
            "model": MODEL,
            "messages": self.conversation_history,
            "system": SYSTEM_PROMPT,
            "stream": False
        }
        try:
            r = requests.post(OLLAMA_URL, json=payload, timeout=30)
            r.raise_for_status()
            response = r.json()["message"]["content"]
            self.conversation_history.append({
                "role": "assistant",
                "content": response
            })
            return response
        except requests.Timeout:
            return "Nya~ sorry, I was thinking too hard and got dizzy... 🌀 try again?"
        except Exception as e:
            return f"Something went wrong~ ({e})"

    def clear_memory(self):
        self.conversation_history = []
        print("🧹 Miss Pretty Kitty forgot everything~ fresh start!")

if __name__ == "__main__":
    mpk = MissPrettyKitty()
    print("\n🐱 Miss Pretty Kitty is ready! Type 'quit' to exit, 'clear' to reset\n")
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Miss Pretty Kitty: Byebye~! 🐱💕")
            break
        if user_input.lower() == "clear":
            mpk.clear_memory()
            continue
        response = mpk.chat(user_input)
        print(f"\nMiss Pretty Kitty: {response}\n")
