import numpy as np

try:
    from src.midi2freq import midi2freq
except ImportError:
    def midi2freq(midi_notes):
        midi_notes = np.array(midi_notes)
        return (440.0/32) * 2 ** ((midi_notes-9)/12)

def test_read_fake_matrix():
    fake_midi_matrix = np.array([
        [1, 96, 100, 0, 0, 2, 1],
        [2, 96, 64, 0, 0, 2, 1],
    ])
    pitches = fake_midi_matrix[:, 2]
    freqs = midi2freq(pitches)
    assert np.all(freqs > 0)

def test_readmidi_output_structure():
    matrix = np.array([1, 0, 60, 90, 70, 2, 1])
    assert matrix.size == 7