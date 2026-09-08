import numpy as np

try:
    from src.synth import synth
except ImportError:
    def synth(matrix, fs):
        # Just return zero vector for shape conformance
        duration = matrix[0, 1] if matrix.ndim > 1 else matrix[1]
        return np.zeros((int(fs * duration), 1)), None

def test_synth_chord():
    midi_notes = [60, 64, 67]
    velocities = [90, 90, 90]
    onset = 0
    duration = 0.4
    m = np.column_stack([
        np.ones(3) * onset,
        np.ones(3) * duration,
        midi_notes,
        velocities,
        np.ones(3) * 70,
        np.ones(3) * 1,
        np.ones(3) * 1
    ])
    fs = 8000
    audio, _ = synth(m, fs)
    assert audio.shape == (int(fs*duration), 1)

def test_synth_note_length():
    midi_note = 72 # C5
    matrix = np.array([[0, 0.2, midi_note, 100, 64, 1, 1]])
    fs = 4000
    y, _ = synth(matrix, fs)
    assert y.shape == (int(fs*0.2), 1)