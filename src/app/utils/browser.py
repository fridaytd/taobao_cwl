import os
import platform

from selenium import webdriver
from fake_useragent import UserAgent


user_agent = UserAgent()


def get_chrome_profile_path():
    """
    Determine the Chrome default profile path based on the operating system
    """
    system = platform.system().lower()

    if system == "windows":
        return os.path.join(
            os.path.expanduser("~"),
            r"AppData\\Local\\Google\\Chrome\\User Data\\",
        )

    elif system == "darwin":  # macOS
        return os.path.join(
            os.path.expanduser("~"), "Library/Application Support/Google/Chrome/"
        )

    elif system == "linux":
        return os.path.join(os.path.expanduser("~"), ".config/google-chrome/")

    else:
        raise OSError(f"Unsupported operating system: {system}")


class BrwDriver(webdriver.Chrome):
    def __init__(self, options=None, service=None, keep_alive=True):
        if options is None:
            options = webdriver.ChromeOptions()

        # adding argument to disable the AutomationControlled flag
        options.add_argument("--disable-blink-features=AutomationControlled")

        # exclude the collection of enable-automation switches
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # turn-off userAutomationExtension
        options.add_experimental_option("useAutomationExtension", False)

        options.add_argument(f"--user-agent={user_agent.random}")

        super().__init__(options, service, keep_alive)

        # changing the property of the navigator value for webdriver to undefined
        self.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

    def random_user_agent(self):
        self.execute_cdp_cmd(
            "Network.setUserAgentOverride", {"userAgent": user_agent.random}
        )

    @staticmethod
    def get_profile_path():
        pass
