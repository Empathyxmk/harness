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

// string input
test('type: handles string argument', async t => {
    const node = createNode('abc');
    await type(node, 'def');
    t.equal(node.textContent, 'def', 'Node text should update to final string');
    t.end();
});

// number input (delay)
test('type: handles number (wait) argument', async t => {
    let waited = false;
    global.setTimeout = fn => { waited = true; fn(); };
    const node = createNode('1');
    await type(node, 30);
    t.ok(waited, 'Should handle wait argument');
    global.setTimeout = realSetTimeout;
    t.end();
});

// function input (async)
test('type: handles async function argument', async t => {
    const node = createNode('foo');
    let called = false;
    async function fakeFn(nodeArg) {
        t.equal(nodeArg, node, 'Function receives node');
        called = true;
    }
    await type(node, fakeFn);
    t.ok(called, 'Should call the function argument');
    t.end();
});

// promise input
test('type: handles promise as argument', async t => {
    const node = createNode('foo');
    let resolved = false;
    const p = new Promise(res => { resolved = true; res(); });
    await type(node, p);
    t.ok(resolved, 'Should await the promise');
    t.end();
});

// workflow input
test('type: performs sequence actions', async t => {
    const node = createNode('');
    await type(node, 'foo', 5, n => type(n, 'bar'));
    t.equal(node.textContent, 'bar', 'Sequence of actions results in correct text');
    t.end();
});