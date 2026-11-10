(function () {
  'use strict';

  function normalizeTag(value) {
    return String(value || '').trim().replace(/\s+/gu, ' ').toLowerCase();
  }

  function uniqueTags(values) {
    const seen = new Set();
    return values.map((value) => String(value || '').trim().replace(/\s+/gu, ' ')).filter((value) => {
      const key = normalizeTag(value);
      if (!key || seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  function applyArticleFilter(document, window) {
    const list = document.getElementById('article-list');
    const nav = document.getElementById('article-tag-filter');
    const empty = document.getElementById('article-tag-empty');
    if (!list || !nav || !empty) return;
    const cards = [...list.querySelectorAll('.editorial-card')];
    if (!cards.length) return;

    const tagsFor = (card) => [...card.querySelectorAll('.tag-chip')].map((link) => link.textContent.slice(1));
    const choices = uniqueTags(cards.flatMap(tagsFor));
    const selected = normalizeTag(new URL(window.location.href).searchParams.get('tag'));
    let visible = 0;
    cards.forEach((card) => {
      const matches = !selected || tagsFor(card).some((tag) => normalizeTag(tag) === selected);
      card.hidden = !matches;
      if (matches) visible += 1;
    });
    empty.hidden = visible !== 0;

    if (!choices.length && !selected) return;
    const addChoice = (label, value) => {
      const link = document.createElement('a');
      const url = new URL(window.location.pathname, window.location.href);
      if (value) url.searchParams.set('tag', value);
      link.href = `${url.pathname}${url.search}`;
      link.textContent = label;
      link.className = 'tag-chip';
      if (normalizeTag(value) === selected) link.setAttribute('aria-current', 'true');
      nav.appendChild(link);
    };
    addChoice(document.documentElement.lang === 'zh-Hant' ? '所有文章' : 'All articles', '');
    choices.forEach((tag) => addChoice(`#${tag}`, tag));
    nav.hidden = false;
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { normalizeTag, uniqueTags, applyArticleFilter };
  } else {
    applyArticleFilter(document, window);
  }
}());
