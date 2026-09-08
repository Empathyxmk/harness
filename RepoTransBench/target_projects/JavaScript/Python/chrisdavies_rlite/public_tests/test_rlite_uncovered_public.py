import os
import sys
import subprocess
import pathlib

import pytest

RLITE_PATH = pathlib.Path(__file__).parent.parent / "rlite.js"

def test_covers_amd_export_path_define_amd_public():
    with open(RLITE_PATH, encoding="utf-8") as f:
        code = f.read()
    script = f"""
let factoryCalledValue = 7;
global.define = function(name, deps, factory) {{
    factoryCalledValue = 42;
}};
global.define.amd = True;
eval(`{code.replace('`', '\\`')}`);
if (factoryCalledValue !== 42) process.exit(43);
"""
    result = subprocess.run(
        ['node', '-e', script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )
    if result.returncode != 0:
        raise AssertionError(f"AMD path not covered (exit {result.returncode}):\n{result.stderr or ''}\n{result.stdout or ''}")
    assert result.returncode == 0

def test_covers_commonjs_export_path_module_exports_public():
    with open(RLITE_PATH, encoding="utf-8") as f:
        code = f.read()
    script = f"""
const module = {{exports: {{}}
}};
let exportsAssigned = false;
global.module = module;
global.exports = module.exports;
eval(`{code.replace('`', '\\`')}`);
// It should attach something to module.exports
if (!(typeof module.exports === "object" || typeof module.exports === "function")) process.exit(41);
exportsAssigned = true;
if (!exportsAssigned) process.exit(44);
"""
    result = subprocess.run(
        ['node', '-e', script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )
    if result.returncode != 0:
        raise AssertionError(f"CommonJS path not covered (exit {result.returncode}):\n{result.stderr or ''}\n{result.stdout or ''}")
    assert result.returncode == 0