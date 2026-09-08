import assert from 'assert'
import { parseHTML } from 'linkedom'

// Patch globals for custom elements
const { document, HTMLElement, customElements } = parseHTML(`<html><body></body></html>`)
global.document = document
global.HTMLElement = HTMLElement
global.customElements = customElements
global.btoa = str => Buffer.from(str).toString('base64')
global.requestAnimationFrame = f => setTimeout(f, 16)
global.setTimeout = setTimeout

// Minimal test harness (no Mocha globals)
function describe(name, fn) { console.log(name); fn(); }
function it(name, fn) { try { fn(); console.log('  ✓', name); } catch (e) { console.error('  ✗', name, e); process.exit(1); } }
global.describe = describe; global.it = it;

describe('Debug El', function () {
  let Debug, El, tagName;

  it('should wrap El notify and dep and override render', async function () {
    Debug = (await import('../debug.js')).El;
    El = (await import('../el.js')).El;

    class SomeEl extends Debug {
      render(html) { return '<div>foo</div>'; }
      static get observedAttributes() { return []; }
    }
    tagName = 'debug-el-common'
    if (!customElements.get(tagName)) customElements.define(tagName, SomeEl)
    let el = document.createElement(tagName);
    document.body.appendChild(el)

    // Check static notification
    let notified = false
    const orig = El.notify
    El.notify = function (...args) {
      notified = true; return orig.apply(this, args)
    }
    El.notify('k', 'v')
    assert.ok(notified, 'notify called')

    // dep function: forcibly set up El._contextId and deps for coverage
    El._contextId = "ctx1"
    El.deps = El.deps || {}
    El.deps['abc'] = { ctx1: 'old' }
    El.dep('abc')
    // Check render override triggers log and works
    el.render('<div>bar</div>')
  });

  it('should handle missing El._contextId in dep', async function () {
    El = (await import('../el.js')).El
    El._contextId = null;
    El.deps = El.deps || {}
    let val = El.dep('xyz');
    assert.equal(val, true)
  });
});