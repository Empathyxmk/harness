'use strict';

const test = require('tape');
const { v4: uuid } = require('uuid');

// Test index.js exports
test('index.js Level exports ClassicLevel', async function (t) {
  // Node.js environment: require index.js
  const { Level } = require('../index.js');
  t.ok(Level, 'Level export exists');
  // Should be a constructor
  t.equal(typeof Level, 'function', 'Level is a constructor');
  // Try constructing and using the main API
  const name = 'db/' + uuid();
  const db = new Level(name);
  t.equal(db.location, name, 'DB location matches');
  await db.put('key1', 'value1');
  const val = await db.get('key1');
  t.equal(val, 'value1', 'put/get round-trip');
  await db.del('key1');
  const afterDel = await db.get('key1').catch(e => e);
  t.ok(afterDel instanceof Error, 'get after delete triggers error');
  await db.close();
  t.end();
});

// Edge case: batch API and chained batch
test('ClassicLevel batch and iterator', async function (t) {
  const { Level } = require('../index.js');
  const name = 'db/' + uuid();
  const db = new Level(name);

  await db.batch([
    { type: 'put', key: 'b', value: '2' },
    { type: 'put', key: 'a', value: '1' },
    { type: 'put', key: 'c', value: '3' }
  ]);

  // Batch get
  const vals = await db.getMany(['a', 'b', 'c']);
  t.deepEqual(vals, ['1', '2', '3']);

  // Chained batch
  const batcher = db.batch();
  batcher.put('x', '10').put('y', '11').del('a');
  await batcher.write();

  const yval = await db.get('y');
  t.equal(yval, '11');

  // Iterator test: fetch all keys
  const keys = [];
  for await (const k of db.keys()) {
    keys.push(k);
  }
  t.ok(keys.includes('b') && keys.includes('c') && keys.includes('x') && keys.includes('y'));

  await db.close();
  t.end();
});