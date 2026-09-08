"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const node_fs_1 = __importDefault(require("node:fs"));
const node_path_1 = __importDefault(require("node:path"));
const minimist_1 = __importDefault(require("minimist"));
const micromatch_1 = __importDefault(require("micromatch"));
const units_1 = __importDefault(require("./units"));
const __1 = __importDefault(require(".."));
const argv = (0, minimist_1.default)(process.argv.slice(2));
const cwd = node_path_1.default.join.bind(node_path_1.default, __dirname, '../benchmark/code');
const files = pattern => {
    const paths = node_fs_1.default.globSync('**/*.js', { cwd: cwd() });
    console.log(paths);
    return (0, micromatch_1.default)(paths, `libs/${pattern}.js`).map(f => cwd(f));
};
if (argv.bench) {
    files(argv.bench).forEach(file => (0, units_1.default)(require(file)));
    return;
}
(0, units_1.default)(__1.default?.default || __1.default);
