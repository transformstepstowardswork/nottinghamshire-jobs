"""Exercise create, edit and delete with build-only content, never real CMS writes."""
from pathlib import Path
import sys


def prepare():
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
    print('Independent fixture creation, editing, deletion and stable distinct URLs verified.')


if __name__ == '__main__':
    {'prepare': prepare, 'check': check}[sys.argv[1]]()
