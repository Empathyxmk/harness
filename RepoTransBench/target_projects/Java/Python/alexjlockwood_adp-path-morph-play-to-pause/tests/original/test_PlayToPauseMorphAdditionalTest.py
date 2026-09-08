import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from src.package_name.PlayToPauseMorph import PlayToPauseMorph

def test_multiple_toggles():
    morph = PlayToPauseMorph(False)
    expected = False
    for _ in range(5):
        morph.toggle()
        expected = not expected
        assert morph.isPlaying() is expected

def test_get_state_strings():
    morph = PlayToPauseMorph(True)
    assert morph.getState() == "PLAY"
    morph.toggle()
    assert morph.getState() == "PAUSE"

def test_edge_case_no_toggle():
    morph_play = PlayToPauseMorph(True)
    assert morph_play.getState() == "PLAY"
    morph_pause = PlayToPauseMorph(False)
    assert morph_pause.getState() == "PAUSE"