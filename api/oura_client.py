import json
import os
import logging
from core.logger import get_logger

logger = get_logger(__name__)


class OuraClient:
    def __init__(self, scenario="default"):
        self.scenario = scenario

    def get_sleep(self):
        filename = "sleep.json" if self.scenario == "default" else f"sleep_{self.scenario}.json"
        return self._load_fixture(filename)

    def get_daily_readiness(self):
        filename = "daily_readiness.json" if self.scenario == "default" else f"readiness_{self.scenario}.json"
        return self._load_fixture(filename)

    def get_daily_activity(self):
        filename = "daily_activity.json" if self.scenario == "default" else f"activity_{self.scenario}.json"
        return self._load_fixture(filename)

    def _load_fixture(self, filename):
        fixture_path = os.path.join(
            os.path.dirname(__file__), "..", "fixtures", filename
        )
        try:
            with open(fixture_path, "r") as f:
                data = json.load(f)
                if not data.get("data"):
                    raise ValueError(f"Empty data in fixture: {filename}")
                return data
        except FileNotFoundError:
            raise RuntimeError(f"Fixture file not found: {filename}")
        except json.JSONDecodeError:
            raise RuntimeError(f"Invalid JSON in fixture: {filename}")