import os
from dotenv import load_dotenv
from google import genai
from anthropic import Anthropic
from api.oura_client import OuraClient

load_dotenv()


class HealthAgent:
    def __init__(self, provider="gemini"):
        self.provider = provider
        self.oura = OuraClient()

        if provider == "claude":
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        elif provider == "gemini":
            self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        else:
            raise ValueError(f"Unsupported provider: {provider}. Choose 'claude' or 'gemini'.")

    def analyze(self):
        sleep = self.oura.get_sleep()
        readiness = self.oura.get_daily_readiness()
        activity = self.oura.get_daily_activity()

        prompt = f"""
        You are a health analyst. Analyze the following Oura Ring health data
        and provide a concise insight with one recommendation.

        Sleep Data: {sleep}
        Readiness Data: {readiness}
        Activity Data: {activity}
        """

        if self.provider == "claude":
            return self._call_claude(prompt)
        elif self.provider == "gemini":
            return self._call_gemini(prompt)

    def _call_claude(self, prompt):
        message = self.client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text

    def _call_gemini(self, prompt):
        response = self.client.models.generate_content(
            model="models/gemini-2.0-flash-lite",
            contents=prompt
        )
        return response.text