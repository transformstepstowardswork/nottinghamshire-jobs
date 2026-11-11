"""Fail closed on unsupported markup in built editorial pages before publication."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import argparse
import sys

BASE = '/'
VOID = {'meta', 'link', 'img', 'br', 'hr'}
TAGS = set('html head body title meta link script a div span header nav main section article footer address p h1 h2 h3 h4 h5 h6 ul ol li blockquote em strong b i s del code pre br hr img time dl dt dd table thead tbody tr th td'.split())
COMMON = {'class', 'id', 'lang', 'title', 'hidden', 'aria-label', 'aria-current', 'aria-hidden', 'aria-describedby', 'data-i18n', 'data-i18n-aria-label', 'data-locale-link', 'data-section-link', 'data-lang-option', 'data-content-locale', 'data-content-section', 'data-site-base', 'data-event', 'data-start', 'data-end', 'data-end-time'}
ATTRS = {
    'a': {'href', 'target', 'rel'}, 'img': {'src', 'alt'}, 'time': {'datetime'},
    'meta': {'charset', 'name', 'content'}, 'link': {'href', 'rel', 'type'},
    'script': {'src', 'defer'}, 'ol': {'start'}, 'th': {'align'}, 'td': {'align'},
}
SCRIPTS = {BASE + 'locale.js', BASE + 'activities.js', BASE + 'articles.js'}
# At the site root, all /paths share a prefix. Preserve the safety boundary
# through a narrow route allowlist instead of accepting any local path.
LOCAL_LINK_PREFIXES = ('/articles/', '/activities/', '/media/images/', '/icons/', '/demos/')
LOCAL_LINK_EXACT = {'/', '/support.html', '/jobs.csv', '/logo_wbg.jpg', '/styles.css', '/manifest.webmanifest'}


def decoded_url(value):
    # Inspect decoded forms too, including encoded colons, control characters and slashes.
    previous = value
    for _ in range(5):
        current = unquote(previous)
        if current == previous:
            break
        previous = current
    if unquote(previous) != previous:
        raise ValueError('excessively encoded URL')
    if not previous or any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in previous) or '\\' in previous:
        raise ValueError('empty URL or URL containing whitespace, controls or backslashes')
    return previous


def check_url(value, page_path, image=False):
    url = decoded_url(value)
    if url.startswith('//'):
        raise ValueError('protocol-relative URL')
    parts = urlsplit(url)
    if parts.scheme:
        if image or parts.scheme.lower() not in {'http', 'https', 'mailto', 'tel'}:
            raise ValueError('unsupported URL scheme')
        if parts.scheme.lower() in {'http', 'https'} and (not parts.hostname or parts.username or parts.password):
            raise ValueError('invalid web URL')
        return
    if parts.netloc:
        raise ValueError('unexpected URL authority')
    target = urlsplit(urljoin('https://editorial.invalid' + page_path, url))
    if target.path not in LOCAL_LINK_EXACT and not target.path.startswith(LOCAL_LINK_PREFIXES):
        raise ValueError('site link leaves allowed public paths')
    if image and not (target.path.startswith(BASE + 'media/images/') or target.path in {BASE + 'icons/apple-touch-icon.png', BASE + 'logo_wbg.jpg'}):
        raise ValueError('image is outside the repository image store')


class EditorialParser(HTMLParser):
    def __init__(self, page_path):
        super().__init__(convert_charrefs=True)
        self.page_path, self.stack, self.errors, self.scripts = page_path, [], [], set()

    def fail(self, message):
        self.errors.append(f'{self.getpos()[0]}: {message}')

    def handle_decl(self, decl):
        if decl.lower() != 'doctype html':
            self.fail('unsupported declaration')

    def unknown_decl(self, data):
        self.fail('unsupported declaration')

    def handle_pi(self, data):
        self.fail('processing instruction is not allowed')

    def handle_comment(self, data):
        self.fail('HTML comments or omitted raw HTML are not supported in editorial content')

    def handle_starttag(self, tag, attrs):
        if tag not in TAGS:
            self.fail(f'unsupported <{tag}> element')
        names = [name for name, _ in attrs]
        if len(names) != len(set(names)):
            self.fail(f'duplicate attribute on <{tag}>')
        attributes = dict(attrs)
        for name, value in attrs:
            if name not in COMMON | ATTRS.get(tag, set()):
                self.fail(f'unsupported {name} attribute on <{tag}>')
            if name in {'href', 'src'}:
                try:
                    check_url(value or '', self.page_path, tag == 'img')
                except ValueError as exc:
                    self.fail(f'unsafe {name} on <{tag}>: {exc}')
        if tag == 'img' and ('alt' not in attributes or not attributes.get('src')):
            self.fail('images need src and alt attributes')
        elif tag == 'img' and not attributes.get('alt') and attributes.get('src') != BASE + 'icons/apple-touch-icon.png':
            self.fail('editorial images need an alt description')
        if tag == 'a' and not attributes.get('href'):
            self.fail('links need an href')
        if tag == 'link' and (self.stack != ['html', 'head'] or attributes.get('href') not in {BASE + 'styles.css', BASE + 'logo_wbg.jpg'}):
            self.fail('unsupported linked resource')
        if tag == 'meta' and (self.stack != ['html', 'head'] or set(attributes) not in ({'charset'}, {'name', 'content'})):
            self.fail('unsupported metadata')
        if tag == 'script':
            src = attributes.get('src')
            if self.stack != ['html', 'head'] or set(attributes) != {'src', 'defer'} or src not in SCRIPTS or src in self.scripts:
                self.fail('unsupported script')
            self.scripts.add(src)
        if tag not in VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID or not self.stack or self.stack[-1] != tag:
            self.fail(f'unbalanced closing </{tag}>')
        else:
            self.stack.pop()

    def handle_data(self, data):
        if self.stack and self.stack[-1] == 'script' and data.strip():
            self.fail('inline script is not allowed')

    def finish(self):
        self.close()
        if self.stack:
            self.fail('unclosed elements')
        if BASE + 'locale.js' not in self.scripts:
            self.fail('expected site script missing')
        return self.errors


def verify(site):
    errors = []
    for section in ('articles', 'activities'):
        directory = site / section
        if not (directory / 'index.html').is_file() or not (directory / 'zh-hant' / 'index.html').is_file():
            errors.append(f'{section}: expected archives missing')
        for path in directory.rglob('*.html'):
            relative = path.relative_to(site).as_posix()
            url = BASE + relative.removesuffix('index.html')
            parser = EditorialParser(url)
            try:
                parser.feed(path.read_text(encoding='utf-8'))
                errors.extend(f'{relative}:{error}' for error in parser.finish())
            except (ValueError, UnicodeError) as exc:
                errors.append(f'{relative}: invalid HTML or encoding: {exc}')
    return errors


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('site', type=Path)
    args = cli.parse_args()
    failures = verify(args.site)
    if failures:
        print('Editorial publication blocked. Correct the indicated content and rebuild:', file=sys.stderr)
        print('\n'.join(failures), file=sys.stderr)
        sys.exit(1)
    print('Editorial HTML verification passed.')
