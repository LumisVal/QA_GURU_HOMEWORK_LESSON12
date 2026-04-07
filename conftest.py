import os
import allure
import pytest

from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def attach_screenshot():
    allure.attach(
        browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=allure.attachment_type.PNG
    )


def attach_page_source():
    allure.attach(
        browser.driver.page_source,
        name='page_source',
        attachment_type=allure.attachment_type.HTML
    )


def attach_browser_logs():
    try:
        logs = browser.driver.get_log("browser")
        log_text = "\n".join(str(log) for log in logs)
        allure.attach(log_text, name='browser_logs', attachment_type=allure.attachment_type.TEXT)
    except Exception:
        pass


def attach_video():
    session_id = browser.driver.session_id
    video_url = f"https://selenoid.autotests.cloud/video/{session_id}.mp4"
    allure.attach(
        f'<html><body><video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4"></video></body></html>',
        name='video',
        attachment_type=allure.attachment_type.HTML
    )


@pytest.fixture(scope='function', autouse=True)
def setup_browser():
    options = Options()
    options.set_capability("browserName", "chrome")
    options.set_capability("selenoid:options", {
        "enableVNC": True,
        "enableVideo": True,
        "name": "demoqa registration test"
    })

    driver = webdriver.Remote(
        command_executor="https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options
    )

    browser.config.driver = driver
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.config.base_url = "https://demoqa.com"

    yield

    attach_screenshot()
    attach_page_source()
    attach_browser_logs()
    attach_video()

    driver.quit()
