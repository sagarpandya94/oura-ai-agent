import os
from dotenv import load_dotenv

load_dotenv()

# LLM Provider
DEFAULT_PROVIDER = os.getenv("LLM_PROVIDER", "claude")

# Model Names
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-opus-4-20250514")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash-lite")

# LLM Settings
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")