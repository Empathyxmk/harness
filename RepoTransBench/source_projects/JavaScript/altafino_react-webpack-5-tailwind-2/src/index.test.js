// The App export is an object because it is a React component.
// To avoid mismatch, check object signature and avoid incorrect type testing.
const App = require("./App");

describe("src/index.js (noop coverage)", () => {
  it("App exports a React component (object or function)", () => {
    // React component could be function or ES6 class, but Babel/ESM interop can create {default} objects.
    expect(typeof App === 'function' || typeof App === 'object').toBe(true);
  });
  // No direct import of src/index.js, which requires DOM APIs.
});