import signal
import pytest

import plop.platform

def test_setitimer_available():
    if hasattr(signal, 'setitimer'):
        # The imported setitimer should match signal's
        assert plop.platform.setitimer == signal.setitimer
    else:
        # If not available, the fallback implementation should exist
        assert hasattr(plop.platform, 'setitimer')
        # Can't easily test fallback behavior in modern python

def test_itimer_constants():
    assert hasattr(plop.platform, 'ITIMER_REAL')
    assert hasattr(plop.platform, 'ITIMER_VIRTUAL')
    assert hasattr(plop.platform, 'ITIMER_PROF')