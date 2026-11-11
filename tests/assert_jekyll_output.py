from pathlib import Path

site = Path('_site')
for name in ['app.js', 'jobs.csv', 'locale.js', 'styles.css', 'logo_wbg.jpg', 'manifest.webmanifest', 'icons/apple-touch-icon.png']:
    assert (site / name).read_bytes() == Path(name).read_bytes(), name
for name in ['index.html', 'support.html']:
    assert (site / name).read_bytes() == Path(name).read_bytes(), name
assert 'fetch(`jobs.csv?updated=' in (site / 'app.js').read_text(encoding='utf-8')
assert 'https://forms.cloud.microsoft/e/7A0mceck5C' in (site / 'support.html').read_text(encoding='utf-8')
en = (site / 'articles/index.html').read_text(encoding='utf-8')
zh = (site / 'articles/zh-hant/index.html').read_text(encoding='utf-8')
assert 'English synthetic sample' in en and '中文測試文章' not in en
assert '中文測試文章' in zh and 'English synthetic sample' not in zh
assert '/articles/en/sample/' in en
article = (site / 'articles/en/sample/index.html').read_text(encoding='utf-8')
chinese = (site / 'articles/zh-hant/sample/index.html').read_text(encoding='utf-8')
activity = (site / 'activities/en/sample/index.html').read_text(encoding='utf-8')
assert '<html lang="zh-Hant"' in chinese
assert '/articles/zh-hant/' in chinese
assert 'Sample heading' in article and 'https://example.org/' in article
assert 'href="javascript:' not in article.lower(), 'Unsafe Markdown link survived rendering'
assert '<script>alert' not in article.lower(), 'Raw script survived rendering'
assert 'alt="Inline example"' in article
assert 'href="javascript:' not in activity.lower()
assert 'Sample image' in article and '/media/images/example.png' in article
assert '/nottinghamshire-jobs/media/images/' not in article, 'Historical CMS image paths must render at the custom-domain root'
assert '/media/images/example.png' in (site / 'articles/index.html').read_text(encoding='utf-8')
assert (site / 'media/images/example.png').read_bytes() == Path('icons/apple-touch-icon.png').read_bytes()
assert not (site / 'tests').exists()
print('Jekyll collections, safe links, language isolation and protected assets verified.')
