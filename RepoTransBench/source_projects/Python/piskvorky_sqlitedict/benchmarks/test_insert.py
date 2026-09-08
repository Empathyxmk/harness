# Skip testing the benchmarks dir in normal test runs.

import pytest

pytest.skip("skip benchmarks dir from test runs", allow_module_level=True)