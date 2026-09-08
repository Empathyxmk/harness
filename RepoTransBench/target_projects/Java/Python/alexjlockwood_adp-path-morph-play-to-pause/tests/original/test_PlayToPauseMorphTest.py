import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.package_name.PlayToPauseMorph import PlayToPauseMorph

def test_initial_state_is_playing():
    morph = PlayToPauseMorph(True)
    assert morph.isPlaying() is True
    assert morph.getState() == "PLAY"

def test_initial_state_is_pause():
    morph = PlayToPauseMorph(False)
    assert morph.isPlaying() is False
    assert morph.getState() == "PAUSE"

def test_toggle_functionality():
    morph = PlayToPauseMorph(True)
    morph.toggle()
    assert morph.isPlaying() is False
    assert morph.getState() == "PAUSE"
    morph.toggle()
    assert morph.isPlaying() is True
    assert morph.getState() == "PLAY"