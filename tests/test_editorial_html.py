import unittest
from scripts.verify_editorial_html import EditorialParser

HEAD = '<!doctype html><html><head><script src="/locale.js" defer></script></head><body>'
TAIL = '</body></html>'


def errors(fragment):
    parser = EditorialParser('/articles/en/sample/')
    parser.feed(HEAD + fragment + TAIL)
    return parser.finish()


class EditorialSafetyTests(unittest.TestCase):
    def test_safe_markdown_output(self):
        self.assertEqual(errors('<h2>Heading</h2><p><strong>Bold</strong> <a href="https://example.org/">link</a></p><ul><li>One</li></ul><img src="/media/images/test.png" alt="Example">'), [])

    def test_rejects_unsafe_urls_and_obfuscation(self):
        for url in ['javascript:alert(1)', 'JaVaScRiPt:alert(1)', '&#x6a;avascript:alert(1)', 'java&#x09;script:alert(1)', 'javascript%3Aalert(1)', '%256aavascript%253aalert(1)', 'data:text/html,hello', '//evil.example/x', '/outside', 'https://example.org\\@evil.test']:
            with self.subTest(url=url):
                self.assertTrue(errors(f'<a href="{url}">link</a>'))

    def test_rejects_active_and_unsupported_html(self):
        for fragment in ['<script>alert(1)</script>', '<iframe src="https://example.org/"></iframe>', '<img src="/media/images/a.png" alt="x" onerror="alert(1)">', '<a href="https://example.org" onclick="alert(1)">x</a>', '<!-- raw HTML omitted -->', '<svg><a href="https://example.org/">x</a></svg>', '<img src="https://evil.test/x.png" alt="x">', '<img src="/media/images/a.png">', '<img src="/media/images/a.png" alt="">', '<a href="https://example.org" href="javascript:alert(1)">x</a>']:
            with self.subTest(fragment=fragment):
                self.assertTrue(errors(fragment))

    def test_rejects_unsupported_metadata_and_inline_script(self):
        self.assertTrue(errors('<meta http-equiv="refresh" content="0;url=https://evil.test">'))
        self.assertTrue(errors('<script src="/locale.js" defer>alert(1)</script>'))
        self.assertTrue(errors('<script src="/articles.js" defer></script>'))

    def test_article_script_is_allowed_only_once_in_head(self):
        parser = EditorialParser('/articles/')
        parser.feed('<!doctype html><html><head><script src="/locale.js" defer></script><script src="/articles.js" defer></script></head><body><a href="/articles/?tag=Career+%26+Training">#Career &amp; Training</a></body></html>')
        self.assertEqual(parser.finish(), [])
        parser = EditorialParser('/articles/')
        parser.feed('<!doctype html><html><head><script src="/locale.js" defer></script><script src="/articles.js" defer></script><script src="/articles.js" defer></script></head><body></body></html>')
        self.assertTrue(parser.finish())


if __name__ == '__main__':
    unittest.main()
