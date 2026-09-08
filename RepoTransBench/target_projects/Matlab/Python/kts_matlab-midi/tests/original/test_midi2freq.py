import pytest
import numpy as np

# Mock or import the midi2freq function from your source code
try:
    from src.midi2freq import midi2freq
except ImportError:
    # Example implementation to allow tests to run - replace with actual implementation
    def midi2freq(midi_notes):
        if isinstance(midi_notes, (list, np.ndarray)):
            midi_notes = np.array(midi_notes)
            return (440.0/32) * 2 ** ((midi_notes-9)/12)
        return (440.0/32) * 2 ** ((midi_notes-9)/12)


class TestMidi2Freq:
    def test_basic_conversion(self):
        # Test a standard MIDI note (A4 = 69) conversion to 440 Hz
        midi_note = 69
        expected_freq = 440
        actual_freq = midi2freq(midi_note)
        assert abs(actual_freq - expected_freq) <= 1e-9

    def test_edge_case_zero(self):
        midi_note = 0
        expected_freq = (440/32)*2**((0-9)/12)
        actual_freq = midi2freq(midi_note)
        assert abs(actual_freq - expected_freq) <= 1e-9

    def test_edge_case_max(self):
        midi_note = 127
        expected_freq = (440/32)*2**((127-9)/12)
        actual_freq = midi2freq(midi_note)
        assert abs(actual_freq - expected_freq) <= 1e-9

    def test_vector_input(self):
        midi_notes = [60, 69, 72]
        expected_freqs = [(440/32)*2**((n-9)/12) for n in midi_notes]
        actual_freqs = midi2freq(midi_notes)
        np.testing.assert_allclose(actual_freqs, expected_freqs, atol=1e-9)