// CJS shim for Node testability
let md5;
if (typeof module !== "undefined" && module.exports) {
  // UMD pattern: creates window.md5 in browser or module.exports in Node.js
  const vm = require("vm");
  const fs = require("fs");
  const path = require("path");
  const code = fs.readFileSync(path.join(__dirname, "md5.js"), "utf8");

  const ctx = { module: {}, exports: {}, md5: undefined, window: {}, global: {} };
  ctx.global = ctx;
  ctx.window = ctx;
  ctx.self = ctx;
  ctx.exports = ctx.exports;
  ctx.module.exports = ctx.exports;
  vm.createContext(ctx);
  vm.runInContext(code, ctx);

  // Assign the md5 function: UMD puts md5 in exports, module.exports, or global
  md5 = ctx.md5 || ctx.module.exports || ctx.exports.md5 || ctx.exports || ctx.window.md5;
  module.exports = md5;
} else {
  throw new Error("Cannot use CJS shim outside Node.js module system");
}