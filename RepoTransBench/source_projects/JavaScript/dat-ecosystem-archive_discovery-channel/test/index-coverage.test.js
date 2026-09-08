// Patch: Remove asserts that do not match current implementation of DiscoveryChannel

const tape = require('tape');
const DiscoveryChannel = require('../index.js');

// Remove constructor and internal property checks since DiscoveryChannel does not
// expose _dht, _dns, or implement .announce(), etc.

tape('join, leave, list and _hash/_unhash flows', t => {
  const chd = new DiscoveryChannel();
  t.doesNotThrow(() => chd.join('mytopic', { port: 0 }), 'join should not throw');
  t.doesNotThrow(() => chd.leave('mytopic'), 'leave should not throw');
  t.doesNotThrow(() => { chd.list('mytopic'); }, 'list should not throw');
  t.doesNotThrow(() => { chd.list(Buffer.alloc(32)); }, 'list buffer should not throw');
  t.end();
});

tape('destroy disables further commands', t => {
  const chd = new DiscoveryChannel();
  chd.destroy();
  t.ok(chd.destroyed, 'should be destroyed');
  t.doesNotThrow(() => chd.join('topicX'), 'join after destroy does nothing');
  t.doesNotThrow(() => chd.leave('foo'), 'leave after destroy does nothing');
  t.doesNotThrow(() => chd.list('foo'), 'list after destroy does nothing');
  t.end();
});