import pytest
import numpy as np
from src.synth import synth

class TestSynth:
    AbsTol = 1e-9

    def test_sine_wave(self):
        freq = 440
        dur = 0.1
        amp = 0.5
        Fs = 44100
        typ = 'sine'
        y = synth(freq, dur, amp, Fs, typ)
        assert y is not None
        assert abs(len(y) - int(np.floor(dur * Fs))) <= 1
        assert np.max(np.abs(y)) <= amp + self.AbsTol

    def test_saw_wave(self):
        freq = 440
        dur = 0.1
        amp = 0.5
        Fs = 44100
        typ = 'saw'
        y = synth(freq, dur, amp, Fs, typ)
        assert y is not None
        assert abs(len(y) - int(np.floor(dur * Fs))) <= 1
        assert np.max(np.abs(y)) <= amp + self.AbsTol

    def test_fm_wave(self):
        freq = 440
        dur = 0.1
        amp = 0.5
        Fs = 44100
        typ = 'fm'
        y = synth(freq, dur, amp, Fs, typ)
        assert y is not None
        assert abs(len(y) - (int(np.floor(dur*Fs)) + 1)) <= 1
        assert np.max(np.abs(y)) <= amp + self.AbsTol

    def test_unknown_type(self):
        freq = 440
        dur = 0.1
        amp = 0.5
        Fs = 44100
        typ = 'unknown'
        with pytest.raises(Exception):
            synth(freq, dur, amp, Fs, typ)

    def test_zero_duration(self):
        freq = 440
        dur = 0.0
        amp = 0.5
        Fs = 44100
        typ = 'sine'
        with pytest.warns(None) as record:
            y = synth(freq, dur, amp, Fs, typ)
        assert y is not None
        assert len(y) == 0

    def test_negative_duration(self):
        freq = 440
        dur = -0.1
        amp = 0.5
        Fs = 44100
        typ = 'sine'
        with pytest.warns(None) as record:
            y = synth(freq, dur, amp, Fs, typ)
        assert y is not None
        assert len(y) == 0

    def test_not_enough_arguments(self):
        with pytest.raises(TypeError):
            synth(440, 0.1, 0.5, 44100)

    def test_smoothing_short_duration(self):
        freq = 440
        dur = 0.01
        amp = 0.5
        Fs = 44100
        typ = 'sine'
        y = synth(freq, dur, amp, Fs, typ)
        N = int(np.floor(dur * Fs))
        n_unsmoothed = np.arange(N)
        y_unsmoothed = amp * np.sin(2 * np.pi * n_unsmoothed * freq / Fs)
        np.testing.assert_allclose(y, y_unsmoothed, atol=1e-9)

    def test_smoothing_long_duration(self):
        freq = 440
        dur = 0.03
        amp = 0.5
        Fs = 44100
        typ = 'sine'
        y = synth(freq, dur, amp, Fs, typ)
        assert abs(y[0]) < 1e-9
        assert abs(y[-1]) < 1e-9
        assert np.max(np.abs(y)) > amp * 0.5