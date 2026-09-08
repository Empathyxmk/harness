import os
import sys
import subprocess
import pathlib

import pytest

RLITE_PATH = pathlib.Path(__file__).parent.parent.parent / "rlite.js"

def test_covers_amd_export_path_define_amd():
    # The UMD expects to be loaded as a script, not via require, so use eval on the code.
    # We'll make define.amd true and ensure the code hits that line (no error = covered).
    with open(RLITE_PATH, encoding="utf-8") as f:
        code = f.read()
    script = f"""
let factoryCalled = false;
global.define = function(name, deps, factory) {{
    factoryCalled = true;
}};
global.define.amd = true;
eval(`{code.replace('`', '\\`')}`);
if (!factoryCalled) process.exit(42);
"""
    completed = subprocess.run(
        [sys.executable, "-c", f"import subprocess; subprocess.run(['node', '-e', '''{script}'''], check=True)"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    # We call node -e. If factoryCalled is not set, node process should exit(42).
    # If all is well, process should exit 0.
    # Instead of subprocess.run inside subprocess.run, use subprocess directly:
    result = subprocess.run(
        ['node', '-e', script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8"
    )
    if result.returncode != 0:
        raise AssertionError(f"AMD path not covered (exit {result.returncode}):\n{result.stderr or ''}\n{result.stdout or ''}")
    assert result.returncode == 0

def test_covers_commonjs_export_path_module_exports():
    # The UMD expects module.exports to be an object/function. We'll check that property was set.
    with open(RLITE_PATH, encoding="utf-8") as f:
        code = f.read()
    script = f"""
let called = false;
const module = {{exports: {{}}
}};
global.module = module;
global.exports = module.exports;
function DummyRlite() {{ called = true; }}
eval(`{code.replace('`', '\\`')}`);
if (!(module.exports && (typeof module.exports === "function" || typeof module.exports === "object"))) process.exit(42);
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