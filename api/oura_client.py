import json
import os

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
        with open(fixture_path, "r") as f:
            return json.load(f)