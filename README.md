## Related Repositories
- [Oura Mock App](https://github.com/sagarpandya94/oura-mock-app) — React Native mock dashboard used for Appium mobile testing

# 🩺 Oura AI Health Agent

An AI-powered agent that fetches and analyzes health data from the Oura Ring API, 
providing intelligent insights on sleep, readiness, and activity trends.

Built by an SDET with a focus on testability, extensibility, and clean architecture.

---

## 🚀 Features

- Fetches Oura health data across sleep, readiness, and activity endpoints
- AI-powered health analysis and personalized recommendations
- Supports multiple LLM providers (Claude and Gemini) — switchable via config
- Fully tested API and agent layers with mocked LLM calls
- Designed to extend into mobile testing (Appium) in future phases

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| AI Providers | Anthropic Claude, Google Gemini |
| API Client | Requests |
| Testing | PyTest |
| Data Validation | JSON Fixtures |
| CI/CD | GitHub Actions (coming soon) |

---

## 📁 Project Structure
```
oura-ai-agent/
├── agents/                  # AI agent logic
│   └── health_agent.py      # Multi-provider health analysis agent
├── api/                     # Oura API client
│   └── oura_client.py       # Fetches sleep, readiness, activity data
├── fixtures/                # Mock API responses for offline testing
│   ├── sleep.json
│   ├── daily_readiness.json
│   └── daily_activity.json
├── tests/
│   ├── api/                 # API layer tests
│   └── agent/               # Agent behavior tests with mocked LLM calls
├── core/                    # Shared config and base classes
├── .env.example             # Environment variable template
└── requirements.txt
```

---

## ⚙️ Setup

**1. Clone the repo**
```bash
git clone https://github.com/<your-username>/oura-ai-agent.git
cd oura-ai-agent
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**
```bash
cp .env.example .env
```
Edit `.env` and add your API keys:
```
ANTHROPIC_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here
```

---

## 🤖 Usage
```python
from agents.health_agent import HealthAgent

# Use Claude
agent = HealthAgent(provider="claude")
print(agent.analyze())

# Use Gemini
agent = HealthAgent(provider="gemini")
print(agent.analyze())
```

---

## 🧪 Running Tests
```bash
# Run all tests
pytest -v

# Run only API tests
pytest tests/api -v

# Run only agent tests
pytest tests/agent -v
```

---

## 🗺️ Roadmap

- [x] Oura API client with fixtures
- [x] Multi-provider AI agent (Claude + Gemini)
- [x] API layer test suite
- [x] Agent layer test suite with mocked LLM calls
- [ ] GitHub Actions CI/CD pipeline
- [ ] OAuth2 Oura API authentication
- [ ] Tool-calling agent with multi-step reasoning
- [ ] Mobile test layer (Appium + Android)

---

## 👤 Author

**Sagar** — Software Development Engineer in Test  
[GitHub](https://github.com/sagarpandya94) • [LinkedIn](https://www.linkedin.com/in/sagarpandya94/)