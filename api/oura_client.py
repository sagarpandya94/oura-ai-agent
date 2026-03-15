import json
import os
import logging

logger = logging.getLogger(__name__)


class OuraClient:

    def get_sleep(self):
        return self._load_fixture("sleep.json")

    def get_daily_readiness(self):
        return self._load_fixture("daily_readiness.json")

    def get_daily_activity(self):
        return self._load_fixture("daily_activity.json")

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