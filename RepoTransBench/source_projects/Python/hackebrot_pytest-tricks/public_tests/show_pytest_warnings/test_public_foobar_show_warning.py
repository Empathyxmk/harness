# -*- coding: utf-8 -*-

import warnings

def test_public_warning_is_shown():
    with warnings.catch_warnings(record=True) as w:
        warnings.warn("this is a public test warning!", UserWarning)
        assert any("public test warning" in str(warning.message) for warning in w)