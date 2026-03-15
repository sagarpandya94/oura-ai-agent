import pytest
from api.oura_client import OuraClient


@pytest.fixture
def client():
    return OuraClient()


class TestSleepData:
    def test_sleep_returns_data(self, client):
        response = client.get_sleep()
        assert "data" in response

    def test_sleep_data_not_empty(self, client):
        response = client.get_sleep()
        assert len(response["data"]) > 0

    def test_sleep_has_required_fields(self, client):
        record = client.get_sleep()["data"][0]
        assert "id" in record
        assert "day" in record
        assert "score" in record

    def test_sleep_score_is_valid(self, client):
        record = client.get_sleep()["data"][0]
        assert 0 <= record["score"] <= 100


class TestReadinessData:
    def test_readiness_returns_data(self, client):
        response = client.get_daily_readiness()
        assert "data" in response

    def test_readiness_has_required_fields(self, client):
        record = client.get_daily_readiness()["data"][0]
        assert "id" in record
        assert "day" in record
        assert "score" in record

    def test_readiness_score_is_valid(self, client):
        record = client.get_daily_readiness()["data"][0]
        assert 0 <= record["score"] <= 100


class TestActivityData:
    def test_activity_returns_data(self, client):
        response = client.get_daily_activity()
        assert "data" in response

    def test_activity_has_required_fields(self, client):
        record = client.get_daily_activity()["data"][0]
        assert "id" in record
        assert "day" in record
        assert "steps" in record

    def test_activity_steps_is_positive(self, client):
        record = client.get_daily_activity()["data"][0]
        assert record["steps"] >= 0