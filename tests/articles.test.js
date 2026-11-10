const test = require('node:test');
const assert = require('node:assert/strict');
const { normalizeTag, uniqueTags } = require('../articles.js');

test('topic matching ignores case and extra whitespace without changing the displayed words', () => {
  assert.equal(normalizeTag('  WoRK  Skills\t'), 'work skills');
  assert.deepEqual(uniqueTags(['  Work  Skills ', 'work skills', 'Career & Training', '', ' 求職 ', '求職']), ['Work Skills', 'Career & Training', '求職']);
});

test('distinct topics are not conflated', () => {
  assert.notEqual(normalizeTag('work skills'), normalizeTag('work-skills'));
  assert.deepEqual(uniqueTags(['C', 'C++', '<Example>']), ['C', 'C++', '<Example>']);
});
