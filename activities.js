(function () {
  'use strict';
  const formatter = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Europe/London', year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
  });

  function londonParts(ms) {
    const p = Object.fromEntries(formatter.formatToParts(new Date(ms)).map(({ type, value }) => [type, value]));
    return { date: `${p.year}-${p.month}-${p.day}`, time: `${p.hour}:${p.minute}` };
  }

  function validDate(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
    const [year, month, day] = value.split('-').map(Number);
    const d = new Date(Date.UTC(year, month - 1, day));
    return d.getUTCFullYear() === year && d.getUTCMonth() === month - 1 && d.getUTCDate() === day;
  }

  function londonEnd(date, time) {
    if (!validDate(date) || !/^([01]\d|2[0-3]):[0-5]\d$/.test(time)) return null;
    const [year, month, day] = date.split('-').map(Number);
    const [hour, minute] = time.split(':').map(Number);
    const nominal = Date.UTC(year, month - 1, day, hour, minute);
    // London uses UTC or UTC+1. For the repeated autumn hour, retain the later instant.
    const matches = [nominal - 3600000, nominal].filter((candidate) => {
      const local = londonParts(candidate);
      return local.date === date && local.time === time;
    });
    return matches.length ? Math.max(...matches) : null;
  }

  function classify(event, now = Date.now()) {
    const start = event.start || '';
    const end = event.end || start;
    const time = event.endTime || '';
    if (!validDate(start) || !validDate(end) || end < start) return 'uncertain';
    if (time) {
      const expiry = londonEnd(end, time);
      return expiry === null ? 'uncertain' : (now > expiry ? 'past' : 'upcoming');
    }
    return londonParts(now).date > end ? 'past' : 'upcoming';
  }

  function arrange(document, now = Date.now()) {
    const all = document.getElementById('events-all');
    if (!all) return;
    const groups = Object.fromEntries(['upcoming', 'uncertain', 'past'].map((name) => [name, document.getElementById(`events-${name}`)]));
    const cards = document.querySelectorAll('[data-event]');
    cards.forEach((card) => {
      const group = groups[classify(card.dataset, now)];
      group.querySelector('.editorial-list').appendChild(card);
    });
    Object.entries(groups).forEach(([name, group]) => {
      const hasCards = Boolean(group.querySelector('[data-event]'));
      group.hidden = name === 'uncertain' && !hasCards;
      const empty = group.querySelector('.event-empty');
      if (empty) empty.hidden = hasCards;
    });
    all.hidden = true;
    const note = document.querySelector('.event-nojs');
    if (note) note.hidden = true;
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { validDate, londonEnd, classify, londonParts };
  } else {
    arrange(document);
    setInterval(() => arrange(document), 30000);
  }
}());
