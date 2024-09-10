#!/bin/env python3

import unittest

import webdriver_assistant as wa


class WebdriverAssistantTest(unittest.TestCase):

    def test_invalid_ca(self):
        with wa.virtual_display_on_linux():
            d = wa.start_chrome_driver(insecure=True)
            d.get('https://cacert.org/')
            self.assertIn('CAcert.org', d.title)
            # wa.preview(d)

    def test_find_element(self):
        with wa.virtual_display_on_linux():
            d = wa.start_chrome_driver()
            d.get('https://example.com/')
            wa.wait_visible(d, 'h1')
            element = wa.find_element_by_css_selector_and_text_match(
                d, 'p a', 'information'
            )
            self.assertIn('More information', element.text)

    def test_form_fill(self):
        with wa.virtual_display_on_linux():
            d = wa.start_chrome_driver()
            d.get('https://www.google.com/')
            wa.wait_visible(d, 'textarea[name="q"]')
            wa.fill_inputs(d, {'textarea[name="q"]': 'manga.club'})
            wa.send_return(d, 'textarea[name="q"]')
            wa.wait_visible(d, 'textarea[name="q"]')
            wa.val(d, 'textarea[name="q"]', '漫画全巻ドットコム', enter=True)


if __name__ == '__main__':
    unittest.main()
