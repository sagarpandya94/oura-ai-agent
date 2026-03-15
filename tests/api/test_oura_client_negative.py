import pytest
from unittest.mock import patch, mock_open
from api.oura_client import OuraClient


@pytest.fixture
def client():
    return OuraClient()


class TestOuraClientErrorHandling:
    def test_missing_fixture_raises_runtime_error(self, client):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(RuntimeError) as exc_info:
                client.get_sleep()
            assert "Fixture file not found" in str(exc_info.value)

    def test_invalid_json_raises_runtime_error(self, client):
        with patch("builtins.open", mock_open(read_data="this is not valid json {{{")):
            with pytest.raises(RuntimeError) as exc_info:
                client.get_sleep()
            assert "Invalid JSON" in str(exc_info.value)

    def test_empty_data_raises_value_error(self, client):
        with patch("builtins.open", mock_open(read_data='{"data": []}')):
            with pytest.raises(ValueError) as exc_info:
                client.get_sleep()
            assert "Empty data" in str(exc_info.value)

    def test_missing_fixture_for_readiness(self, client):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(RuntimeError) as exc_info:
                client.get_daily_readiness()
            assert "Fixture file not found" in str(exc_info.value)

    def test_missing_fixture_for_activity(self, client):
        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(RuntimeError) as exc_info:
                client.get_daily_activity()
            assert "Fixture file not found" in str(exc_info.value)