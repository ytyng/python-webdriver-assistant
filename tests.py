import unittest

import webdriver_assistant as wa


class WebdriverAssistantTest(unittest.TestCase):

    def test_invalid_ca(self):
        with wa.virtual_display_on_linux():
            d = wa.start_chrome_driver(insecure=True)
            d.get('https://cacert.org/')
            self.assertIn('CAcert.org', d.title)
            # wa.preview(d)


if __name__ == '__main__':
    unittest.main()
