"""Check built public entry points, unchanged feed/assets and local resource URLs."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

try:
    from .validate_job_update import validate_csv_bytes, ValidationError
except ImportError:  # Direct CLI execution from scripts/.
    from validate_job_update import validate_csv_bytes, ValidationError

BASE = '/nottinghamshire-jobs/'
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ('app.js', 'jobs.csv', 'locale.js', 'articles.js', 'activities.js',
          'demos/my-next-step-en.html', 'demos/my-next-step-zh-hant.html',
          'styles.css', 'logo_wbg.jpg', 'manifest.webmanifest',
          'icons/apple-touch-icon.png', 'icons/app-icon-192.png', 'icons/app-icon-512.png')
ARCHIVES = ('articles/index.html', 'articles/zh-hant/index.html',
            'activities/index.html', 'activities/zh-hant/index.html')


class LocalResources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value and (name == 'src' or (name == 'href' and tag == 'link')):
                self.urls.append(value)


def verify(site, source=ROOT):
    errors = []
    for name in (*ASSETS, 'index.html', 'support.html'):
        path = site / name
        if not path.is_file() or path.read_bytes() != (source / name).read_bytes():
            errors.append(f'{name}: missing or changed from checked-out source')
    for name in ARCHIVES:
        if not (site / name).is_file():
            errors.append(f'{name}: expected language archive missing')
    for name in ('tests', 'scripts', '.git', '.github', 'PAGES_RUNBOOK.md'):
        if (site / name).exists():
            errors.append(f'{name}: internal source must not enter public output')
    if (site / 'support.html').is_file():
        support = (site / 'support.html').read_text(encoding='utf-8')
        if 'https://forms.cloud.microsoft/e/7A0mceck5C' not in support:
            errors.append('support.html: expected enquiry destination missing')
    for path in site.rglob('*.html'):
        text = path.read_text(encoding='utf-8')
        parser = LocalResources()
        parser.feed(text)
        page_url = BASE + path.relative_to(site).as_posix()
        for value in parser.urls:
            parts = urlsplit(value)
            if parts.scheme or parts.netloc:
                continue
            target = unquote(urlsplit(urljoin(page_url, value)).path)
            if not target.startswith(BASE) or not (site / target[len(BASE):]).is_file():
                errors.append(f'{path.relative_to(site)}: missing local resource {value}')
    # The same structural/security CSV contract used by weekly Job Updates.
    try:
        result = validate_csv_bytes((site / 'jobs.csv').read_bytes())
        print(f'Public feed: {result}')
    except (ValidationError, OSError) as exc:
        errors.append(f'jobs.csv: {exc}')
    return errors


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('site', type=Path)
    args = cli.parse_args()
    errors = verify(args.site)
    if errors:
        cli.exit(1, 'Public site verification failed:\n' + '\n'.join(errors) + '\n')
    print('Public entry points, archives, local assets, Forms link and unchanged feed verified.')
