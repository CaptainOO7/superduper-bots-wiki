import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { test } from 'node:test'

test('public FAQ keeps unique stable IDs and a versioned answer for each question', () => {
  const text = readFileSync(new URL('../docs/faq/index.md', import.meta.url), 'utf8')
  assert.match(text, /^# 常见问题\n/)
  const entries = text.split(/^## /m).slice(1).map(section => /^(FAQ-\d{3}) [^\n]+\n([\s\S]+)$/.exec(section))
  assert.ok(entries.every(Boolean))
  const ids = entries.map(entry => entry[1])
  assert.equal(ids.length, new Set(ids).size)
  for (const id of ['FAQ-001', 'FAQ-002', 'FAQ-003']) assert.ok(ids.includes(id), id)
  for (const entry of entries) assert.match(entry[2], /适用版本：/)
})
