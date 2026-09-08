'use strict';

const test = require('tape');
const { v4: uuid } = require('uuid');

// Public test for index.js exports with different data
test('index.js Level exports ClassicLevel (public)', async function (t) {
  // Node.js environment: require index.js
  const { Level } = require('../index.js');
  t.ok(Level, 'Level export exists (public)');
  // Should be a constructor
  t.equal(typeof Level, 'function', 'Level is a constructor (public)');
  // Different DB name and different put/get key/value data
  const name = 'db/' + uuid();
  const db = new Level(name);
  t.equal(db.location, name, 'DB location matches (public)');
  await db.put('key2', 'value42');
  const val = await db.get('key2');
  t.equal(val, 'value42', 'put/get round-trip (public)');
  await db.del('key2');
  const afterDel = await db.get('key2').catch(e => e);
  t.ok(afterDel instanceof Error, 'get after delete triggers error (public)');
  await db.close();
  t.end();
});

// Public test: batch API and chained batch with different keys/values
test('ClassicLevel batch and iterator (public)', async function (t) {
  const { Level } = require('../index.js');
  const name = 'db/' + uuid();
  const db = new Level(name);

  // Use different data order and values compared to original test
  await db.batch([
    { type: 'put', key: 'd', value: '7' },
    { type: 'put', key: 'z', value: '99' },
    { type: 'put', key: 'm', value: '0' }
  ]);

  // Batch get with different order
  const vals = await db.getMany(['z', 'd', 'm']);
  t.deepEqual(vals, ['99', '7', '0'], 'batch getMany with public data');

  // Chained batch with different keys/values and delete a different key
  const batcher = db.batch();
  batcher.put('u', '101').put('v', '202').del('z');
  await batcher.write();

  const vval = await db.get('v');
  t.equal(vval, '202', 'get value after chained put (public)');

  // Iterator test: fetch all keys and check public set of keys
  const keys = [];
  for await (const k of db.keys()) {
    keys.push(k);
  }
  t.ok(keys.includes('d') && keys.includes('m') && keys.includes('u') && keys.includes('v'), 'iterator found expected keys (public)');

  await db.close();
  t.end();
});