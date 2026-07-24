# src/llm_client.py
from groq import Groq
from src.config import GROQ_API_KEY, LLM_MODEL

class GroqLLM:
    def __init__(self, model=LLM_MODEL):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = model
        print(f"Connected to Groq LLM: {model}")

    def generate(self, prompt: str, context: str, chat_history: list = None) -> str:
        """
        Context aur history ke saath answer generate karein
        """
        # System prompt
        system_msg = """You are a helpful AI Research Assistant.
Answer the user's question based ONLY on the provided context.
If the answer is not in the context, say "I don't have enough information to answer that."
Always cite your sources by referring to the source numbers provided in the context."""

        # Build messages
        messages = [{"role": "system", "content": system_msg}]

        # Add chat history if exists
        if chat_history:
            messages.extend(chat_history)

        # Add current context + question
        user_msg = f"""Context (with source numbers):\n{context}\n\nQuestion: {prompt}\n\nProvide a clear, accurate answer based on the context above. Cite sources like [Source 1], [Source 2] etc."""

        messages.append({"role": "user", "content": user_msg})

        # Generate
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,  # Factual answers ke liye low temperature
            max_tokens=1024,
            top_p=0.9
        )

        return response.choices[0].message.content

# Test
if __name__ == "__main__":
    llm = GroqLLM()
    test_context = "[Source 1]: AI is transforming healthcare. [Source 2]: Machine learning helps diagnose diseases."
    answer = llm.generate("How is AI used in healthcare?", test_context)
    print(f"Answer: {answer}")
