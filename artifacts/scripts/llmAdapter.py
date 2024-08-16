from abc import ABC, abstractmethod
from PromptGenerator import PromptGenerator
from anthropic import Anthropic
from openai import OpenAI
import google.generativeai as genai

OPEN_AI_KEY = ""
CLAUDE_KEY = ""
GOOGLE_KEY = ""

class LlmApi:
    def __init__(self, model: str, max_output_tokens: int, prompt_type: int):
        self.max_output_tokens = max_output_tokens
        self.promptGenerator = PromptGenerator(prompt_type=prompt_type)
        if model.startswith("claude"):
            self.adapter = AnthropicAdapter(api_key=CLAUDE_KEY, model=model, max_output_tokens=max_output_tokens)
        elif model.startswith("gpt"):
            self.adapter = OpenAIAdapter(api_key=OPEN_AI_KEY, model=model, max_output_tokens=max_output_tokens)
        elif model.startswith("gemini"):
            self.adapter = GoogleAdapter(api_key=GOOGLE_KEY, model=model)

    def call(self, issue: dict) -> str:
        prompt = self.promptGenerator.generate_prompt(issue)
        return self.adapter.call(prompt)


class LLMAdapter(ABC):
    @abstractmethod
    def call(self, prompt: str) -> str:
        pass

class AnthropicAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str, max_output_tokens: int):
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.max_output_tokens = max_output_tokens

    def call(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_output_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

class OpenAIAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str, max_output_tokens: int):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_output_tokens = max_output_tokens

    def call(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            max_tokens=self.max_output_tokens
        )
        return response.choices[0].message.content

class GoogleAdapter(LLMAdapter):
    def __init__(self, api_key: str, model: str):
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)

    def call(self, prompt: str) -> str:
        safe = [
            {
                "category": "HARM_CATEGORY_DANGEROUS",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE",
            },
        ]
        response = self.client.generate_content(prompt, safety_settings=safe)
        return response.text