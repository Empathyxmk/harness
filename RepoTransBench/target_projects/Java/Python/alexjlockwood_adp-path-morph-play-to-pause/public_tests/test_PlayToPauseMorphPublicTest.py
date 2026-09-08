import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.package_name.PlayToPauseMorph import PlayToPauseMorph

def test_initial_state_is_pause_public():
    morph = PlayToPauseMorph(False)
    assert morph.isPlaying() is False
    assert morph.getState() == "PAUSE"

def test_initial_state_is_playing_public():
    morph = PlayToPauseMorph(True)
    assert morph.isPlaying() is True
    assert morph.getState() == "PLAY"

def test_double_toggle_functionality_public():
    morph = PlayToPauseMorph(False)
    morph.toggle()
    assert morph.isPlaying() is True
    assert morph.getState() == "PLAY"
    morph.toggle()
    assert morph.isPlaying() is False
    assert morph.getState() == "PAUSE"