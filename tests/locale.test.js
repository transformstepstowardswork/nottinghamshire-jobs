const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const {
  COPY,
  localeFromSearch,
  localizedUrl,
  normalizeLocale
} = require('../locale.js');

test('locale parsing defaults safely to English and accepts Traditional Chinese', () => {
  assert.equal(normalizeLocale('en'), 'en');
  assert.equal(normalizeLocale('zh-Hant'), 'zh-Hant');
  assert.equal(normalizeLocale('ZH-hant'), 'zh-Hant');
  assert.equal(normalizeLocale('fr'), 'en');
  assert.equal(localeFromSearch('?lang=zh-Hant'), 'zh-Hant');
  assert.equal(localeFromSearch('?lang=unsupported'), 'en');
  assert.equal(localeFromSearch(''), 'en');
});

test('localized URLs preserve the working route and remove the default language parameter', () => {
  const base = 'https://transformstepstowardswork.github.io/nottinghamshire-jobs/support.html?from=jobs';
  assert.equal(
    localizedUrl('./', 'zh-Hant', base),
    '/nottinghamshire-jobs/?lang=zh-Hant'
  );
  assert.equal(
    localizedUrl('support.html?lang=zh-Hant', 'en', base),
    '/nottinghamshire-jobs/support.html'
  );
  assert.equal(
    localizedUrl('./#main-content', 'zh-Hant', base),
    '/nottinghamshire-jobs/?lang=zh-Hant#main-content'
  );
});

test('Jobs and Support expose only static locale hooks and the shared language shell', () => {
  const index = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
  const support = fs.readFileSync(path.join(__dirname, '..', 'support.html'), 'utf8');
  const locale = fs.readFileSync(path.join(__dirname, '..', 'locale.js'), 'utf8');

  assert.match(index, /locale\.js" defer><\/script>[\s\S]*app\.js" defer>/);
  assert.match(support, /locale\.js" defer><\/script>/);
  assert.match(index, /data-lang-option="zh-Hant"/);
  assert.match(support, /data-lang-option="zh-Hant"/);
  assert.match(index, /data-locale-link/);
  assert.match(support, /data-locale-link/);
  assert.match(support, /data-locale-copy-pending="zh-Hant"/);
  assert.match(support, /https:\/\/forms\.cloud\.microsoft\/e\/7A0mceck5C/);
  assert.doesNotMatch(locale, /MutationObserver/);
  assert.doesNotMatch(locale, /querySelectorAll\('\[data-locale-copy-pending/);

  const keys = new Set();
  for (const markup of [index, support]) {
    assert.match(markup, /<a class="brand"[^>]*data-locale-link/);
    assert.match(markup, /<a class="skip-link" href="#main-content" data-i18n="nav\.skip"/);
    assert.match(markup, /id="main-content"/);
    for (const match of markup.matchAll(/data-i18n(?:-[a-z-]+)?="([^"]+)"/g)) {
      keys.add(match[1]);
    }
  }
  assert.equal(COPY.en['brand.aria'], 'Transform Jobs by Transform Training');
  assert.match(index, /<strong>Transform Jobs<\/strong>/);
  assert.match(support, /<strong>Transform Jobs<\/strong>/);
  assert.match(index, /apple-mobile-web-app-title" content="Transform Jobs"/);
  assert.match(support, /apple-mobile-web-app-title" content="Transform Jobs"/);
  assert.match(support, /demos\/my-next-step-en\.html/);
  assert.match(support, /demos\/my-next-step-zh-hant\.html/);
  assert.match(support, /support\.previewAccess/);
  assert.match(support, /data-locale-copy-pending="zh-Hant"/);
  assert.match(COPY.en['support.previewAccess'], /only available to people enrolled in Steps Towards Work/);
  assert.match(COPY['zh-Hant']['support.previewAccess'], /Steps Towards Work/);
  assert.equal(COPY['zh-Hant']['nav.skip'], '跳至主要內容');
  assert.doesNotMatch(Object.values(COPY['zh-Hant']).join(' '), /洛定咸/);
  for (const key of keys) {
    assert.ok(COPY.en[key], `English locale is missing ${key}`);
    assert.ok(COPY['zh-Hant'][key], `Traditional Chinese locale is missing ${key}`);
  }
});
