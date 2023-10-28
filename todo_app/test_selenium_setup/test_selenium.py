import pytest
from selenium import webdriver
 
# Module scope re-uses the fixture
@pytest.fixture(scope='module')
def driver():
    # path to your webdriver download
    # leave this empty if you want Selenium to download it for you
    with webdriver.Chrome() as driver:
        yield driver
 
def test_python_home(driver):
    driver.get("https://www.python.org")
    assert driver.title == 'Welcome to Python.org'