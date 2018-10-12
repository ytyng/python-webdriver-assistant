import os
import time
from typing import Union, Optional

from selenium.webdriver import Chrome, ChromeOptions, DesiredCapabilities

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


class BrowserTimeout(Exception):
    pass


def start_display_on_linux():
    """
    Ubuntu の場合、仮想フレームバッファを起動する
    """
    import platform
    if platform.system() != 'Linux':
        return
    try:
        from pyvirtualdisplay import Display
    except ImportError:
        return

    display = Display(visible=0, size=(1280, 800))
    display.start()
    return display


default_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) ' \
                     'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                     'Chrome/67.0.3396.99 Safari/537.36'


def start_chrome_driver(
        *, headless: Union[str, bool] = 'auto',
        user_agent: Optional[bool] = None,
        insecure: bool = False) -> WebDriver:
    options = ChromeOptions()

    def _is_headless_mode():
        if headless == 'auto':
            import sys
            if 'test' in sys.argv:
                return True
        return headless

    if _is_headless_mode():
        # ヘッドレスモードを有効にする
        options.add_argument('--headless')
    options.add_argument('--lang=ja')
    options.add_argument('--ignore-certificate-errors')  # 多分意味ない
    if user_agent is None:
        user_agent = default_user_agent
    options.add_argument(
        '--user-agent=' + user_agent)

    capabilities = DesiredCapabilities.CHROME
    if insecure:
        capabilities['acceptSslCerts'] = True  # 多分意味ない
        capabilities['acceptInsecureCerts'] = True  # 効く

    driver = Chrome(options=options, desired_capabilities=capabilities)
    return driver


def preview(driver: WebDriver, filename_prefix: str = None) -> None:
    """
    画像とHTMLでプレビュー
    """
    import subprocess
    import tempfile

    tmpdir = tempfile.gettempdir()
    filename_prefix = filename_prefix or 'webdriver-assistant-preview'
    png_path = os.path.join(tmpdir, '{}.png'.format(filename_prefix))
    html_path = os.path.join(tmpdir, '{}.html'.format(filename_prefix))

    driver.save_screenshot(png_path)

    subprocess.Popen(['open', png_path])
    with open(html_path, 'w') as fp:
        fp.write(driver.page_source)
    subprocess.Popen(['open', html_path])


def wait_visible(driver: WebDriver, css_selector: str,
                 timeout: int = 3000) -> None:
    """
    エレメントが表示されるまで待つ
    """
    for i in range(int(timeout / 100)):
        e = driver.find_element_by_css_selector(css_selector)
        if e.is_displayed():
            return
        time.sleep(0.1)
    raise BrowserTimeout(css_selector)


def find_element_or_none(
        driver: WebDriver, css_selector: str
) -> Optional[WebElement]:
    """
    エレメントを取得、もしくは None
    """
    try:
        return driver.find_element_by_css_selector(css_selector)
    except WebDriverException:
        return None


def build_requests_session(driver: WebDriver):
    import requests
    from requests.cookies import create_cookie

    s = requests.session()
    s.headers['User-Agent'] = default_user_agent
    for cookie in driver.get_cookies():
        c = create_cookie(**{
            'name': cookie['name'],
            'value': cookie['value'],
            'domain': cookie['domain'],
            'path': cookie['path'],
            'expires': cookie['expiry'],
            'secure': cookie['secure'],
            'rest': {'HttpOnly': cookie['httpOnly'], },
        })
        s.cookies.set_cookie(c)

    return s


def fill_inputs(driver: WebDriver, data: dict) -> None:
    for key, value in data.items():
        e = find_element_or_none(driver, key)
        if not e:
            continue
        e.send_keys(value)


def send_return(driver: WebDriver, css_selector: str) -> None:
    e = find_element_or_none(driver, css_selector)
    if not e:
        return
    e.send_keys(Keys.RETURN)
