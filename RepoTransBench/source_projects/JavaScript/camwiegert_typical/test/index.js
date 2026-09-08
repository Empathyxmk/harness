const test = require('tape');
const typical = require('../typical.js');

const writer = typical.writer;
const deleter = typical.deleter;
const editor = typical.editor;
const getOverlap = typical.getOverlap;

// Only require functions that actually exist
const hasType = typeof typical.type === "function";
const hasEdit = typeof typical.edit === "function";
const hasWait = typeof typical.wait === "function";
const hasPerform = typeof typical.perform === "function";

test('deleter: Should create an iterable', (t) => {
  const steps = Array.from(deleter('abc'));
  t.deepEqual(steps, ['ab', 'a', ''], 'Should create an array');
  t.end();
});

test('deleter: Should create correct steps', (t) => {
  const steps = Array.from(deleter('ab'));
  t.deepEqual(
    steps.map(s => typeof s),
    ['string', 'string'],
    'Each step is string'
  );
  t.end();
});

test('deleter: Should handle empty string', (t) => {
  const steps = Array.from(deleter(''));
  t.equal(steps.length, 0, 'No steps for empty');
  t.end();
});

test('deleter: Should handle startIndex', (t) => {
  const steps = Array.from(deleter('abc', 1));
  t.equal(steps.length, 2, 'Only 2 steps for partial');
  t.end();
});

test('deleter: Should handle endIndex', (t) => {
  const steps = Array.from(deleter('abc', 0, 2));
  t.equal(steps.length, 2, '2 steps for partial end');
  t.end();
});

test('deleter: Should handle emoji', (t) => {
  const steps = Array.from(deleter('😊👍'));
  t.deepEqual(steps, ['😊', ''], 'Handles emoji');
  t.end();
});

test('editor: Should create an iterable', (t) => {
  const result = editor(['a', 'b']);
  t.ok(result && typeof result[Symbol.iterator] === 'function', 'Iterable editor');
  t.end();
});

test('editor: Should have correct length', (t) => {
  const steps = Array.from(editor(['a', 'b']));
  t.ok(steps.length > 0, 'Nonzero steps');
  t.end();
});

test('editor: Should yield functions', (t) => {
  const steps = Array.from(editor(['a', 'b']));
  t.ok(steps.every(x => typeof x === 'function'), 'All steps functions');
  t.end();
});

test('getOverlap: partial overlap', (t) => {
  t.equal(getOverlap('abc', 'abd'), 2, 'Overlap index correct');
  t.end();
});

test('getOverlap: no overlap', (t) => {
  t.equal(getOverlap('abc', 'xyz'), 0, 'No overlap');
  t.end();
});

test('getOverlap: complete overlap', (t) => {
  t.equal(getOverlap('abc', 'abc'), 3, 'Complete overlap');
  t.end();
});

test('getOverlap: write only', (t) => {
  t.equal(getOverlap('', 'foo'), 0, 'Write only');
  t.end();
});

test('getOverlap: delete only', (t) => {
  t.equal(getOverlap('bar', ''), 0, 'Delete only');
  t.end();
});

test('getOverlap: emoji', (t) => {
  t.equal(getOverlap('😊😊', '😊😎'), 1, 'Emoji');
  t.end();
});

test('writer: Should create an iterable', (t) => {
  const steps = Array.from(writer('ab'));
  t.ok(Array.isArray(steps), 'Iterable writer');
  t.end();
});

test('writer: Should create correct steps', (t) => {
  const steps = Array.from(writer('ab'));
  t.deepEqual(steps, ['a', 'ab'], '2 steps created');
  t.end();
});

test('writer: Should handle empty string', (t) => {
  const steps = Array.from(writer(''));
  t.equal(steps.length, 0, 'No steps empty');
  t.end();
});

test('writer: Should handle startIndex', (t) => {
  const steps = Array.from(writer('abc', 1));
  t.deepEqual(steps, ['ab', 'abc'], 'Partial startIndex steps');
  t.end();
});

test('writer: Should handle endIndex', (t) => {
  const steps = Array.from(writer('abc', 0, 2));
  t.deepEqual(steps, ['a', 'ab'], '2 steps for endIndex');
  t.end();
});

test('writer: Should handle emoji', (t) => {
  const steps = Array.from(writer('😊👍'));
  t.deepEqual(steps, ['😊', '😊👍'], 'Handles emoji');
  t.end();
});

// Conditionally run tests for functions only if they exist

if (hasType) {
  test('type: string arg', async (t) => {
    let called = false;
    global.requestAnimationFrame = (cb) => { called = true; cb(); return 1; };
    let node = { textContent: 'foo' };
    await typical.type(node, 'bar');
    t.ok(called, 'requestAnimationFrame called');
    t.equal(node.textContent, 'bar', 'Node edited to bar');
    t.end();
  });

  test('type: number arg (wait)', async (t) => {
    let node = { textContent: 'foo' };
    const before = Date.now();
    await typical.type(node, 10);
    const elapsed = Date.now() - before;
    t.ok(elapsed >= 9, 'Waited at least 9ms');
    t.end();
  });

  test('type: function arg (callback)', async (t) => {
    let node = { textContent: 'x' };
    let cbCalled = false;
    async function cb(nd) {
      cbCalled = true;
      nd.textContent = 'y';
    }
    await typical.type(node, cb);
    t.ok(cbCalled, 'Function argument called');
    t.equal(node.textContent, 'y', 'Node edited by function');
    t.end();
  });

  test('type: default (object/non-primitive)', async (t) => {
    let node = { textContent: 'z' };
    let obj = Promise.resolve();
    await typical.type(node, obj);
    t.equal(node.textContent, 'z', 'Node unchanged');
    t.end();
  });
}

if (hasEdit) {
  test('edit: edits text', async (t) => {
    let called = false;
    global.requestAnimationFrame = (cb) => { called = true; cb(); return 1; };
    let node = { textContent: 'foo' };
    await typical.edit(node, 'foo', 'bar');
    t.equal(node.textContent, 'bar', 'Edit works end-to-end');
    t.end();
  });
}

if (hasWait) {
  test('wait: delays', async (t) => {
    const before = Date.now();
    await typical.wait(20);
    const elapsed = Date.now() - before;
    t.ok(elapsed >= 18, 'Delayed for at least 18ms');
    t.end();
  });
}

if (hasPerform) {
  test('perform: step through', async (t) => {
    let waits = [];
    global.setTimeout = (f, ms) => { waits.push(ms); f(); };
    global.requestAnimationFrame = (cb) => (cb(), 1);
    let node = { textContent: '' };
    await typical.perform(node, ['a', 'ab'], 1);
    t.equal(node.textContent, 'ab', 'Performed all ops');
    t.end();
  });
}