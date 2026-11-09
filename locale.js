(function () {
  'use strict';

  const DEFAULT_LOCALE = 'en';
  const TRADITIONAL_CHINESE_LOCALE = 'zh-Hant';

  const COPY = {
    en: {
      'meta.jobsDescription': 'Search current paid vacancies from local councils, NHS organisations, universities, schools, academy trusts, charities and voluntary/community organisations.',
      'meta.jobsTitle': 'Nottinghamshire Job Opportunities | Transform Training',
      'meta.supportDescription': 'Support from Transform Training to help you build confidence, develop skills and move forward.',
      'meta.supportTitle': 'Job-search support | Nottinghamshire Jobs | Transform Training',
      'brand.aria': 'Nottinghamshire Jobs by Transform Training',
      'brand.byTransform': 'by Transform Training',
      'language.selector': 'Language selector',
      'language.label': 'Language:',
      'nav.main': 'Main navigation',
      'nav.skip': 'Skip to main content',
      'nav.jobs': 'Jobs',
      'nav.support': 'Get support',
      'footer.nav': 'Transform Training information',
      'jobs.eyebrow': 'Current local opportunities',
      'jobs.title': 'Find a job in Nottinghamshire',
      'jobs.lede': 'Search recently checked vacancies from local councils, NHS organisations, universities, schools, charities and community organisations.',
      'jobs.currentVacancies': 'current vacancies',
      'jobs.lastChecked': 'Last checked',
      'jobs.supportNudgeTitle': 'Need a bit more help with your job search?',
      'jobs.supportNudgeBody': 'Transform Training can support people who want help taking their next step.',
      'jobs.seeSupport': 'See support',
      'jobs.guidance': 'This list is checked regularly by Transform Training. Short summaries help you understand the role, but always read the employer’s official advert before applying because vacancies can close early or change.',
      'jobs.searchSection': 'Search and filter jobs',
      'jobs.searchLegend': 'Search and filter jobs',
      'jobs.searchLabel': 'Search job title or keyword',
      'jobs.searchPlaceholder': 'Search job title, organisation or keyword',
      'jobs.filters': 'Filters',
      'jobs.sort': 'Sort',
      'jobs.sortClosingSoonest': 'Closing soonest',
      'jobs.sortOrganisation': 'Organisation A–Z',
      'jobs.sortTitle': 'Job title A–Z',
      'jobs.sortClosingLatest': 'Closing latest',
      'jobs.narrowList': 'Narrow the list',
      'jobs.clearFilters': 'Clear filters',
      'jobs.jobArea': 'Job area',
      'jobs.allJobAreas': 'All job areas',
      'jobs.location': 'Location',
      'jobs.allLocations': 'All locations',
      'jobs.workPattern': 'Work pattern',
      'jobs.anyWorkPattern': 'Any work pattern',
      'jobs.organisation': 'Organisation',
      'jobs.allOrganisations': 'All organisations',
      'jobs.resultsDescription': 'Showing current vacancies from the latest checked list.',
      'jobs.reset': 'Reset search & filters',
      'footer.title': 'Transform Training',
      'footer.copy': 'Practical support to help people build confidence, develop skills and move forward.',
      'footer.official': 'Official website',
      'footer.support': 'Get job-search support',
      'footer.terms': 'Terms & Privacy',
      'footer.legalUpdate': 'This job list is updated regularly by Transform Training. Vacancies can close early or be withdrawn, so always check the employer’s official advert before applying.',
      'footer.legalRegistration': 'Transform Training Ltd is a company limited by guarantee registered in England and Wales, company number 08929034, and a registered charity in England and Wales, charity number 1158831.',
      'support.eyebrow': 'Support from Transform Training',
      'support.backToJobs': '← Back to Nottinghamshire Jobs'
    },
    'zh-Hant': {
      'meta.jobsDescription': '搜尋來自地方議會、國民保健服務、院校、學校、學院信託、慈善機構及志願／社區組織的現有有薪職位。',
      'meta.jobsTitle': '諾定咸郡職位機會 | Transform Training',
      'meta.supportDescription': 'Transform Training 提供支援，協助你建立信心、發展技能並繼續前行。',
      'meta.supportTitle': '求職支援 | 諾定咸郡職位 | Transform Training',
      'brand.aria': '由 Transform Training 提供的諾定咸郡職位',
      'brand.byTransform': '由 Transform Training 提供',
      'language.selector': '語言選擇',
      'language.label': '語言：',
      'nav.main': '主要導覽',
      'nav.skip': '跳至主要內容',
      'nav.jobs': '職位',
      'nav.support': '獲取支援',
      'footer.nav': 'Transform Training 資訊',
      'jobs.eyebrow': '本地最新機會',
      'jobs.title': '在諾定咸郡尋找工作',
      'jobs.lede': '搜尋來自地方議會、國民保健服務、院校、學校、慈善機構及社區組織的近期核實職位。',
      'jobs.currentVacancies': '個現有職位',
      'jobs.lastChecked': '最近檢查',
      'jobs.supportNudgeTitle': '需要更多求職協助？',
      'jobs.supportNudgeBody': 'Transform Training 可以支援希望踏出下一步的人士。',
      'jobs.seeSupport': '查看支援',
      'jobs.guidance': 'Transform Training 定期檢查這份清單。簡短摘要有助你了解職位，但申請前請務必閱讀僱主的官方招聘廣告，因為職位可能提早截止或有所更改。',
      'jobs.searchSection': '搜尋及篩選職位',
      'jobs.searchLegend': '搜尋及篩選職位',
      'jobs.searchLabel': '搜尋職位名稱或關鍵字',
      'jobs.searchPlaceholder': '搜尋職位名稱、機構或關鍵字',
      'jobs.filters': '篩選',
      'jobs.sort': '排序',
      'jobs.sortClosingSoonest': '最先截止',
      'jobs.sortOrganisation': '機構 A–Z',
      'jobs.sortTitle': '職位名稱 A–Z',
      'jobs.sortClosingLatest': '最遲截止',
      'jobs.narrowList': '縮小清單',
      'jobs.clearFilters': '清除篩選',
      'jobs.jobArea': '職位類別',
      'jobs.allJobAreas': '所有職位類別',
      'jobs.location': '地點',
      'jobs.allLocations': '所有地點',
      'jobs.workPattern': '工作模式',
      'jobs.anyWorkPattern': '任何工作模式',
      'jobs.organisation': '機構',
      'jobs.allOrganisations': '所有機構',
      'jobs.resultsDescription': '顯示最新檢查清單中的現有職位。',
      'jobs.reset': '重設搜尋及篩選',
      'footer.title': 'Transform Training',
      'footer.copy': '實際支援，協助人們建立信心、發展技能並繼續前行。',
      'footer.official': '官方網站',
      'footer.support': '獲取求職支援',
      'footer.terms': '條款及私隱',
      'footer.legalUpdate': '這份職位清單由 Transform Training 定期更新。職位可能提早截止或被撤回，因此申請前請務必查看僱主的官方招聘廣告。',
      'footer.legalRegistration': 'Transform Training Ltd 是一家在英格蘭及威爾斯註冊的擔保有限公司，註冊公司編號 08929034，亦是英格蘭及威爾斯的註冊慈善機構，慈善編號 1158831。',
      'support.eyebrow': 'Transform Training 提供的支援',
      'support.backToJobs': '← 返回諾定咸郡職位'
    }
  };

  const ATTRIBUTE_COPY = {
    'data-i18n-aria-label': 'aria-label',
    'data-i18n-placeholder': 'placeholder',
    'data-i18n-content': 'content'
  };

  function normalizeLocale(value) {
    return String(value ?? '').trim().toLowerCase() === 'zh-hant'
      ? TRADITIONAL_CHINESE_LOCALE
      : DEFAULT_LOCALE;
  }

  function localeFromSearch(search) {
    return normalizeLocale(new URLSearchParams(String(search ?? '')).get('lang'));
  }

  function localizedUrl(href, locale, baseHref = 'https://example.test/') {
    const url = new URL(href, baseHref);
    const nextLocale = normalizeLocale(locale);
    if (nextLocale === DEFAULT_LOCALE) {
      url.searchParams.delete('lang');
    } else {
      url.searchParams.set('lang', nextLocale);
    }
    return `${url.pathname}${url.search}${url.hash}`;
  }

  function copyFor(locale, key) {
    return COPY[locale]?.[key] ?? COPY[DEFAULT_LOCALE]?.[key] ?? '';
  }

  function applyAttributeCopy(document, locale) {
    Object.entries(ATTRIBUTE_COPY).forEach(([dataAttribute, attribute]) => {
      document.querySelectorAll(`[${dataAttribute}]`).forEach((element) => {
        const value = copyFor(locale, element.getAttribute(dataAttribute));
        if (value) {
          element.setAttribute(attribute, value);
        }
      });
    });
  }

  function applyLocale(document, window, locale = localeFromSearch(window.location.search)) {
    const activeLocale = normalizeLocale(locale);
    document.documentElement.setAttribute('lang', activeLocale);
    document.documentElement.setAttribute('data-locale', activeLocale);

    document.querySelectorAll('[data-i18n]').forEach((element) => {
      const value = copyFor(activeLocale, element.getAttribute('data-i18n'));
      if (value) {
        element.textContent = value;
      }
    });
    applyAttributeCopy(document, activeLocale);

    const currentUrl = new URL(window.location.href);
    document.querySelectorAll('[data-locale-link]').forEach((link) => {
      const href = link.getAttribute('href');
      if (!href) {
        return;
      }
      const target = new URL(href, currentUrl);
      if (target.origin === currentUrl.origin) {
        link.setAttribute('href', localizedUrl(href, activeLocale, currentUrl.href));
      }
    });

    document.querySelectorAll('[data-lang-option]').forEach((link) => {
      const optionLocale = normalizeLocale(link.getAttribute('data-lang-option'));
      const href = link.getAttribute('href') || currentUrl.pathname;
      link.setAttribute('href', localizedUrl(href, optionLocale, currentUrl.href));
      if (optionLocale === activeLocale) {
        link.setAttribute('aria-current', 'true');
        link.classList.add('is-current');
      } else {
        link.removeAttribute('aria-current');
        link.classList.remove('is-current');
      }
    });

    return activeLocale;
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
      COPY,
      DEFAULT_LOCALE,
      TRADITIONAL_CHINESE_LOCALE,
      applyLocale,
      copyFor,
      localeFromSearch,
      localizedUrl,
      normalizeLocale
    };
    return;
  }

  applyLocale(document, window);
}());
