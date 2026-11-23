"""Exercise create, edit and delete with build-only content, never real CMS writes."""
from pathlib import Path
import sys


def prepare():
    cases = {
        'source-only': 'source_name: Plain source\nsource_url: http://example.org/source\n',
        'author-only': 'author_name: Sole author\n',
        'url-only': 'source_url: https://example.org/hidden\n',
        'blank-credit': 'author_name: "   "\nsource_name: "   "\nsource_url: "   "\n',
        'unsafe-credit': 'author_name: Credited author\nsource_name: Unsafe source\nsource_url: javascript:alert(1)\n',
    }
    for name, fields in cases.items():
        Path(f'_articles_en/{name}.md').write_text(
            f'---\ntitle: {name}\ndate: 2026-11-01\n{fields}---\n\nCredit fixture.\n', encoding='utf-8')
    en = Path('_articles_en/sample.md')
    original = en.read_text(encoding='utf-8')
    Path('_articles_en/sample-2.md').write_text(original, encoding='utf-8')
    en.write_text(original.replace('English synthetic sample', 'Edited English fixture'), encoding='utf-8')
    Path('_articles_zh/sample.md').unlink()
    chinese = Path('_activities_zh/sample.md')
    original = chinese.read_text(encoding='utf-8')
    Path('_activities_zh/sample-2.md').write_text(original, encoding='utf-8')
    chinese.write_text(original.replace('中文測試活動', '已修改活動'), encoding='utf-8')
    Path('_activities_en/sample.md').unlink()


def check():
    site = Path('_site')
    en_archive = (site / 'articles/index.html').read_text(encoding='utf-8')
    zh_archive = (site / 'articles/zh-hant/index.html').read_text(encoding='utf-8')
    en_activity = (site / 'activities/index.html').read_text(encoding='utf-8')
    zh_activity = (site / 'activities/zh-hant/index.html').read_text(encoding='utf-8')
    assert 'Edited English fixture' in en_archive and 'English synthetic sample' in en_archive
    assert '/articles/en/sample/' in en_archive and '/articles/en/sample-2/' in en_archive
    assert 'Edited English fixture' in (site / 'articles/en/sample/index.html').read_text(encoding='utf-8')
    assert 'English synthetic sample' in (site / 'articles/en/sample-2/index.html').read_text(encoding='utf-8')
    assert '中文測試文章' not in zh_archive and not (site / 'articles/zh-hant/sample/index.html').exists()
    assert 'Synthetic activity' not in en_activity and not (site / 'activities/en/sample/index.html').exists()
    assert '已修改活動' in zh_activity and '中文測試活動' in zh_activity
    assert '/activities/zh-hant/sample/' in zh_activity and '/activities/zh-hant/sample-2/' in zh_activity
    source_only = (site / 'articles/en/source-only/index.html').read_text(encoding='utf-8')
    assert 'Source: <a href="http://example.org/source">Plain source</a>' in source_only
    assert '<span>By ' not in source_only and ' · ' not in source_only
    author_only = (site / 'articles/en/author-only/index.html').read_text(encoding='utf-8')
    assert 'By Sole author' in author_only and 'Source:' not in author_only
    for name in ('url-only', 'blank-credit'):
        html = (site / f'articles/en/{name}/index.html').read_text(encoding='utf-8')
        assert 'class="article-credit"' not in html
        assert 'https://example.org/hidden' not in html
    unsafe = (site / 'articles/en/unsafe-credit/index.html').read_text(encoding='utf-8')
    assert 'By Credited author' in unsafe and 'Source: Unsafe source' in unsafe
    assert 'javascript:' not in unsafe
    print('Independent fixture creation, editing, deletion and stable distinct URLs verified.')


if __name__ == '__main__':
    {'prepare': prepare, 'check': check}[sys.argv[1]]()
