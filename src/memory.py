# src/memory.py
class ConversationMemory:
    def __init__(self, max_history: int = 5):
        """
        Last N messages yaad rakhein for context
        """
        self.max_history = max_history
        self.messages = []

    def add_message(self, role: str, content: str):
        """Message add karein"""
        self.messages.append({"role": role, "content": content})

        if len(self.messages) > self.max_history * 2:
            self.messages = self.messages[-self.max_history * 2:]

    def get_history(self):
        """Chat history return karein LLM ke liye"""
        return self.messages.copy()

    def clear(self):
        """Memory clear karein"""
        self.messages = []

    def get_summary(self):
        """Quick summary for display"""
        return f"{len(self.messages)//2} messages in memory"
