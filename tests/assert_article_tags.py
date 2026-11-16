from collections import Counter
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
fixture_en = ['#Work Skills', '#Career & Training', '#<Example>', '#work skills']
fixture_zh = ['#求職', '#社區', '#求職']

# Real CMS articles legitimately add tags; check fixed fixtures separately.
assert not Counter(fixture_en) - Counter(text for _, text in en), en
assert not Counter(fixture_zh) - Counter(text for _, text in zh), zh
for href, text in en + zh:
    parsed = urlsplit(href)
    assert parse_qs(parsed.query)['tag'] == [text[1:]], (href, text)
    assert parsed.path.startswith('/articles/')
assert [text for _, text in chips('_site/articles/en/sample/index.html')] == fixture_en[:3]
assert [text for _, text in chips('_site/articles/zh-hant/sample/index.html')] == fixture_zh[:2]
assert [text for _, text in chips('_site/articles/en/shared/index.html')] == fixture_en[3:]
assert [text for _, text in chips('_site/articles/zh-hant/shared/index.html')] == fixture_zh[2:]
assert not chips('_site/articles/en/untagged/index.html')
assert not chips('_site/articles/zh-hant/untagged/index.html')
print('Locale-specific, deduplicated, escaped article topics and shareable links verified.')
