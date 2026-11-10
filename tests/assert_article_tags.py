from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


class Chips(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.active = None

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'a' and 'tag-chip' in values.get('class', '').split():
            self.active = [values['href'], '']

    def handle_data(self, text):
        if self.active is not None:
            self.active[1] += text

    def handle_endtag(self, tag):
        if tag == 'a' and self.active is not None:
            self.links.append(self.active)
            self.active = None


def chips(path):
    parser = Chips()
    parser.feed(Path(path).read_text(encoding='utf-8'))
    return parser.links


en = chips('_site/articles/index.html')
zh = chips('_site/articles/zh-hant/index.html')
assert [text for _, text in en] == ['#Work Skills', '#Career & Training', '#<Example>'], en
assert [text for _, text in zh] == ['#求職', '#社區'], zh
for href, text in en + zh:
    parsed = urlsplit(href)
    assert parse_qs(parsed.query)['tag'] == [text[1:]], (href, text)
    assert parsed.path.startswith('/nottinghamshire-jobs/articles/')
assert chips('_site/articles/en/sample/index.html') == en
assert chips('_site/articles/zh-hant/sample/index.html') == zh
assert not chips('_site/articles/en/untagged/index.html')
assert not chips('_site/articles/zh-hant/untagged/index.html')
print('Locale-specific, deduplicated, escaped article topics and shareable links verified.')
