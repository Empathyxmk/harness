"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const tsup_1 = require("tsup");
exports.default = (0, tsup_1.defineConfig)({
    clean: true,
    entry: ['index.ts'],
    cjsInterop: true,
    format: ['cjs', 'esm'],
    keepNames: true,
    minify: false,
    shims: true,
    splitting: false,
    sourcemap: true,
    target: 'node20'
});
