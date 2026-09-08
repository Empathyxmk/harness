import numpy as np

try:
    from src.midi2freq import midi2freq
except ImportError:
    def midi2freq(midi_notes):
        midi_notes = np.array(midi_notes)
        return (440.0/32) * 2 ** ((midi_notes-9)/12)

def test_A440_to_freq():
    # C5 (MIDI 72): 440 * 2^((72-69)/12) = 523.2511 Hz
    freq = midi2freq(72)
    assert abs(round(freq, 1) - 523.3) <= 0.1

def test_range_of_notes():
    midi_notes = np.array([48, 55, 62])
    expected = midi2freq([48, 55, 62])
    actual = midi2freq(midi_notes)
    np.testing.assert_allclose(actual, expected, atol=1e-6)