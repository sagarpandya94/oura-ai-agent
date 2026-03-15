import pytest
from api.oura_client import OuraClient


@pytest.mark.parametrize("scenario,expected_sleep_score", [
    ("default", 82),
    ("poor", 45),
    ("excellent", 95),
])
def test_sleep_score_matches_scenario(scenario, expected_sleep_score):
    client = OuraClient(scenario=scenario)
    data = client.get_sleep()
    assert data["data"][0]["score"] == expected_sleep_score


@pytest.mark.parametrize("scenario,expected_readiness_score", [
    ("default", 74),
    ("poor", 35),
    ("excellent", 92),
])
def test_readiness_score_matches_scenario(scenario, expected_readiness_score):
    client = OuraClient(scenario=scenario)
    data = client.get_daily_readiness()
    assert data["data"][0]["score"] == expected_readiness_score


@pytest.mark.parametrize("scenario,expected_steps", [
    ("default", 8200),
    ("poor", 2100),
    ("excellent", 15000),
])
def test_activity_steps_matches_scenario(scenario, expected_steps):
    client = OuraClient(scenario=scenario)
    data = client.get_daily_activity()
    assert data["data"][0]["steps"] == expected_steps


@pytest.mark.parametrize("scenario", ["default", "poor", "excellent"])
def test_all_scenarios_return_valid_schema(scenario):
    client = OuraClient(scenario=scenario)

    sleep = client.get_sleep()
    assert "data" in sleep
    assert "score" in sleep["data"][0]

    readiness = client.get_daily_readiness()
    assert "data" in readiness
    assert "score" in readiness["data"][0]

    activity = client.get_daily_activity()
    assert "data" in activity
    assert "steps" in activity["data"][0]


@pytest.mark.parametrize("scenario", ["default", "poor", "excellent"])
def test_all_scenarios_scores_within_valid_range(scenario):
    client = OuraClient(scenario=scenario)

    sleep_score = client.get_sleep()["data"][0]["score"]
    readiness_score = client.get_daily_readiness()["data"][0]["score"]
    activity_score = client.get_daily_activity()["data"][0]["score"]

    assert 0 <= sleep_score <= 100
    assert 0 <= readiness_score <= 100
    assert 0 <= activity_score <= 100