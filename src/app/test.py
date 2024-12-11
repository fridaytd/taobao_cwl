import os
import time

from app.utils.logger import logger
from app.utils.browser import BrwDriver, get_chrome_profile_path
from selenium import webdriver

options = webdriver.ChromeOptions()

profile_path = get_chrome_profile_path()
print(profile_path)

options.add_argument(f"user-data-dir={os.path.dirname(profile_path)}")
options.add_argument("--profile-directory=Default")

driver = BrwDriver(options=options)


driver.get("https://google.com")
print(driver.execute_script("return navigator.userAgent;"))
time.sleep(1)
driver.random_user_agent()
driver.get("https://codeforces.com")
print(driver.execute_script("return navigator.userAgent;"))
driver.random_user_agent()
print(driver.execute_script("return navigator.userAgent;"))

print(get_chrome_profile_path())
print("sleeping")
time.sleep(1000)
