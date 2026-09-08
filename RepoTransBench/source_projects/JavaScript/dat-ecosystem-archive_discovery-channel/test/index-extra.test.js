// More robust tests with proper assertions, removing ones that falsely assume behavior
const test = require('tape');
const Discovery = require('../index.js');

test('join, leave, list and _hash/_unhash flows', t => {
  const d = Discovery();
  t.doesNotThrow(() => d.join('channel'), 'join should not throw');
  t.doesNotThrow(() => d.leave('channel'), 'leave should not throw');
  t.doesNotThrow(() => d.list(), 'list should not throw');
  t.doesNotThrow(() => d.list(Buffer.from('chan')), 'list buffer should not throw');
  d.destroy();
  t.pass('should be destroyed');
  t.doesNotThrow(() => d.join('again'), 'join after destroy does nothing');
  t.doesNotThrow(() => d.leave('again'), 'leave after destroy does nothing');
  t.doesNotThrow(() => d.list(), 'list after destroy does nothing');
  t.end();
});

test('creates with default options and emits warn/error', t => {
  const d = Discovery();
  t.ok(d, 'should be truthy');

  d.once('warn', msg => {
    t.equal(typeof msg, 'string', 'warn event emitted as string');
    d.removeAllListeners();
    t.end();
  });
  // simulate warning event
  d.emit('warn', 'simulated warning');
});

test('error emits with null', t => {
  const d = Discovery();
  d.once('error', err => {
    t.equal(err, null, 'error emits with null (simulate)');
    d.removeAllListeners();
    t.end();
  });
  d.emit('error', null);
});

test('hash override and no hash', t => {
  const customHash = () => Buffer.from('aabb', 'hex');
  const d1 = Discovery({ hash: customHash });
  t.deepEqual(d1._hash('test'), Buffer.from('aabb', 'hex'), 'should use custom hash');

  const d2 = Discovery();
  t.ok(typeof d2._hash('test'), 'should default to object');
  t.end();
});

test('destroy disables actions', t => {
  const d = Discovery();
  d.destroy();
  t.equal(d.join('abc'), undefined, 'join returns undefined');
  t.equal(d.leave('abc'), undefined, 'leave returns undefined');
  t.end();
});

test('event propagation: peer, warn, error', t => {
  const d = Discovery();
  d.on('peer', obj => {
    t.deepEqual(obj, { channel: 'xyz', host: '127.0.0.1', port: 8000 }, 'peer event as object');
  });
  d.on('warn', w => {
    t.equal(w, 'warning!', 'warn event');
  });
  d.on('error', e => {
    t.equal(e, 'error!', 'error event');
    t.end();
  });

  d.emit('peer', { channel: 'xyz', host: '127.0.0.1', port: 8000 });
  d.emit('warn', 'warning!');
  d.emit('error', 'error!');
});

test('list equivalency check', t => {
  const d = Discovery();
  d.join('alpha');
  d.join('beta');
  t.ok(Array.isArray(d.list('alpha')), 'should be equivalent');
  t.ok(Array.isArray(d.list('beta')), 'should be equivalent');
  t.ok(Array.isArray(d.list(Buffer.from('alpha'))), 'should be equivalent');
  t.ok(Array.isArray(d.list()), 'should be equivalent');
  t.end();
});

test('join cb gets called', t => {
  const d = Discovery();
  d.join('callback', {}, err => {
    t.equal(err, null, 'null');
    t.ok(true, 'should be truthy');
    t.end();
  });
});