const test = require('node:test');
const assert = require('node:assert/strict');
const { classify, londonEnd } = require('../activities.js');

test('date-only and unknown-end events remain current through the London day', () => {
  const event = { start: '2026-07-01', end: '', endTime: '' };
  assert.equal(classify(event, Date.parse('2026-07-01T22:59:59Z')), 'upcoming');
  assert.equal(classify(event, Date.parse('2026-07-01T23:00:00Z')), 'past');
});

test('known end time expires without a build and uses summer or winter offset', () => {
  const summer = { start: '2026-07-01', endTime: '15:00' };
  assert.equal(classify(summer, Date.parse('2026-07-01T14:00:00Z')), 'upcoming');
  assert.equal(classify(summer, Date.parse('2026-07-01T14:00:01Z')), 'past');
  assert.equal(londonEnd('2026-12-01', '15:00'), Date.parse('2026-12-01T15:00:00Z'));
});

test('ambiguous autumn time uses the later instant; invalid and missing dates stay uncertain', () => {
  assert.equal(londonEnd('2026-10-25', '01:30'), Date.parse('2026-10-25T01:30:00Z'));
  assert.equal(londonEnd('2026-03-29', '01:30'), null);
  assert.equal(classify({ start: '2026-03-29', endTime: '01:30' }, Date.parse('2027-01-01')), 'uncertain');
  assert.equal(classify({ start: '2026-02-30' }, Date.parse('2027-01-01')), 'uncertain');
  assert.equal(classify({ start: '' }, Date.parse('2027-01-01')), 'uncertain');
});
