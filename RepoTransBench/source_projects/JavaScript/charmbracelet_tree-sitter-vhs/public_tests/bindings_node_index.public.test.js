const nodeIndexPath = require('path').join(__dirname, "../bindings/node/index.js");

// Use a module-scoped variable for assertion!
let expectedRootForPublicTest = null;

// Patch global.process inside the test so the mock can access this variable outside the jest.mock factory.
describe("public test: node-gyp-build loading (public scenario)", () => {
  it("should call node-gyp-build with the project root directory (public scenario)", () => {
    expectedRootForPublicTest = require('path').resolve(__dirname, "..");
    jest.resetModules();
    jest.doMock("node-gyp-build", () => {
      // Only use variables or globals accessible in factory scope.
      const path = require('path');
      return function(root) {
        // Use the outer variable for assertion (it will be set before loading the module)
        if (expectedRootForPublicTest !== null) {
          // Delay requiring expect until runtime, outside jest.mock factory!
          require('assert').strictEqual(path.resolve(root), expectedRootForPublicTest);
        }
        return { __publicTest: true, calledWith: root };
      };
    });

    const mod = require(nodeIndexPath);
    expect(mod.__publicTest).toBe(true);
    expect(require('path').resolve(mod.calledWith)).toBe(expectedRootForPublicTest);
    expectedRootForPublicTest = null;
  });
});