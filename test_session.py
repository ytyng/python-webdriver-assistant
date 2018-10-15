import os
import unittest

import webdriver_assistant as wa


class WebdriverAssistantTest(unittest.TestCase):

    @wa.virtual_display_on_linux()
    def test_session(self):
        if not os.environ.get('MANGAZENKAN_PASSWORD'):
            return
        # wa.start_display_on_linux()
        d = wa.start_chrome_driver(headless=False)
        d.get('https://www.mangazenkan.com/mypage/login.php')

        wa.fill_inputs(d, {
            'input[name="mypage_login_email"]':
                os.environ['MANGAZENKAN_EMAIL'],
            'input[name="mypage_login_pass"]':
                os.environ['MANGAZENKAN_PASSWORD'],
        })

        wa.send_return(d, 'input[name="mypage_login_pass"]')

        session = wa.build_requests_session(d)
        response = session.get('https://www.mangazenkan.com/mypage/')
        self.assertTrue(response.ok)
        self.assertIn('購入履歴一覧', response.content.decode())


if __name__ == '__main__':
    unittest.main()
