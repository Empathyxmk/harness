const test = require('tape');
const { type } = require('../typical.js');

// Fake node for testing
function createNode(text) {
    return { textContent: text };
}

// Patch requestAnimationFrame
global.requestAnimationFrame = cb => cb();

// Patch setTimeout to be synchronous for testing
const realSetTimeout = global.setTimeout;
global.setTimeout = (fn, ms) => { fn(); };

// string input (different values)
test('type: handles string argument (public)', async t => {
    const node = createNode('xyz');
    await type(node, 'uvw');
    t.equal(node.textContent, 'uvw', 'Node text should update to new string');
    t.end();
});

// number input (delay) with a different value
test('type: handles different wait argument (public)', async t => {
    let waited = false;
    global.setTimeout = fn => { waited = true; fn(); };
    const node = createNode('2');
    await type(node, 42);
    t.ok(waited, 'Should handle different wait argument');
    global.setTimeout = realSetTimeout;
    t.end();
});

// function input (async) with alternate function
test('type: handles different async function argument (public)', async t => {
    const node = createNode('bar');
    let called = false;
    async function fakeFnB(nodeArg) {
        t.equal(nodeArg, node, 'Function receives correct node');
        called = true;
    }
    await type(node, fakeFnB);
    t.ok(called, 'Should call the different function argument');
    t.end();
});

// promise input (with a slightly different promise)
test('type: handles different promise as argument (public)', async t => {
    const node = createNode('baz');
    let resolved = false;
    const p = new Promise(res => { setTimeout(() => { resolved = true; res(); }, 0); });
    await type(node, p);
    t.ok(resolved, 'Should await the different promise');
    t.end();
});

// sequence workflow with different steps
test('type: performs public sequence actions', async t => {
    const node = createNode('');
    await type(node, 'abc', 10, n => type(n, 'xyz'));
    t.equal(node.textContent, 'xyz', 'Public sequence of actions results in correct text');
    t.end();
});