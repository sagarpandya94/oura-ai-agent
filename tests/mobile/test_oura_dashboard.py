import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


@pytest.fixture(scope="module")
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "emulator-5554"
    options.app_package = "com.ouramockapp"
    options.app_activity = ".MainActivity"
    options.no_reset = True

    driver = webdriver.Remote("http://localhost:4723", options=options)
    yield driver
    driver.quit()


class TestOuraDashboard:
    def test_date_is_displayed(self, driver):
        date = driver.find_element(AppiumBy.XPATH, '//*[@resource-id="app-date"]')
        assert date.is_displayed()
        assert date.text == "March 13, 2025"

    def test_sleep_card_is_displayed(self, driver):
        card = driver.find_element(AppiumBy.XPATH, '//*[@resource-id="sleep-card"]')
        assert card.is_displayed()

    def test_sleep_score_is_correct(self, driver):
        score = driver.find_element(AppiumBy.XPATH, '//*[@resource-id="sleep-card-score"]')
        assert score.text == "82"

    def test_sleep_title_is_correct(self, driver):
        title = driver.find_element(AppiumBy.XPATH, '//*[@resource-id="sleep-card-title"]')
        assert title.text == "Sleep"

    def test_readiness_card_is_displayed(self, driver):
        card = driver.find_element(AppiumBy.XPATH, '//*[@resource-id="readiness-card"]')
        assert card.is_displayed()

    def test_readiness_score_is_correct(self, driver):
        score = driver.find_element(AppiumBy.XPATH, '//*[@resource-id="readiness-card-score"]')
        assert score.text == "74"

    def test_activity_card_is_displayed(self, driver):
        card = driver.find_element(AppiumBy.XPATH, '//*[@resource-id="activity-card"]')
        assert card.is_displayed()

    def test_activity_score_is_correct(self, driver):
        score = driver.find_element(AppiumBy.XPATH, '//*[@resource-id="activity-card-score"]')
        assert score.text == "67"

    def test_steps_are_displayed(self, driver):
        detail = driver.find_element(AppiumBy.XPATH, '//*[@resource-id="activity-card-detail-0"]')
        assert "8,200" in detail.text