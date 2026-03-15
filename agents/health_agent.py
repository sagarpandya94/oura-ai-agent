import os
from dotenv import load_dotenv
from google import genai
from anthropic import Anthropic
from api.oura_client import OuraClient
from core.config import CLAUDE_MODEL, GEMINI_MODEL, MAX_TOKENS

load_dotenv()

from core.logger import get_logger
logger = get_logger(__name__)


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
        try:
            sleep = self.oura.get_sleep()
            readiness = self.oura.get_daily_readiness()
            activity = self.oura.get_daily_activity()
        except RuntimeError as e:
            logger.error(f"Failed to fetch health data: {e}")
            raise

        prompt = f"""
        You are a health analyst. Analyze the following Oura Ring health data
        and provide a concise insight with one recommendation.

        Sleep Data: {sleep}
        Readiness Data: {readiness}
        Activity Data: {activity}
        """

        try:
            if self.provider == "claude":
                return self._call_claude(prompt)
            elif self.provider == "gemini":
                return self._call_gemini(prompt)
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise RuntimeError(f"Failed to get response from {self.provider}: {e}")

    def _call_claude(self, prompt):
        response = self.client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS,
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.content[0].text
        if not result:
            raise RuntimeError("Claude returned an empty response")
        return result

    def _call_gemini(self, prompt):
        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        result = response.text
        if not result:
            raise RuntimeError("Gemini returned an empty response")
        return result