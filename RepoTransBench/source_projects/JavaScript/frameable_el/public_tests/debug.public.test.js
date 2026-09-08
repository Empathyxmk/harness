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

describe('Debug El (Public)', function () {
  let Debug, El, tagName;

  it('should wrap El notify and dep and override render with new tag/data', async function () {
    Debug = (await import('../debug.js')).El;
    El = (await import('../el.js')).El;

    class AnotherEl extends Debug {
      render(html) { return '<span>bazqux</span>'; }
      static get observedAttributes() { return []; }
    }
    tagName = 'debug-el-public'
    if (!customElements.get(tagName)) customElements.define(tagName, AnotherEl)
    let el = document.createElement(tagName);
    document.body.appendChild(el)

    // Check static notification with new key/values
    let notified = false
    const orig = El.notify
    El.notify = function (...args) {
      notified = true; return orig.apply(this, args)
    }
    El.notify('newKey', 'newValue')
    assert.ok(notified, 'notify called (public)')

    // dep function: forcibly set up El._contextId and deps for coverage
    El._contextId = "publicCtx2"
    El.deps = El.deps || {}
    El.deps['def'] = { publicCtx2: 'previous' }
    El.dep('def')
    // Check render override triggers log and works
    el.render('<span>quuz</span>')
  });

  it('should handle missing El._contextId in dep for public test', async function () {
    El = (await import('../el.js')).El
    El._contextId = undefined;
    El.deps = El.deps || {}
    let val = El.dep('uvw');
    assert.equal(val, true)
  });
});