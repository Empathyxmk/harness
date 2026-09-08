import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.package_name.PlayToPauseMorph import PlayToPauseMorph

def test_multiple_toggles_public():
    morph = PlayToPauseMorph(True)
    expected = True
    for _ in range(4):
        morph.toggle()
        expected = not expected
        assert morph.isPlaying() is expected

def test_get_state_strings_public():
    morph = PlayToPauseMorph(False)
    assert morph.getState() == "PAUSE"
    morph.toggle()
    assert morph.getState() == "PLAY"

def test_edge_case_no_toggle_public():
    morph_pause = PlayToPauseMorph(False)
    assert morph_pause.getState() == "PAUSE"
    morph_play = PlayToPauseMorph(True)
    assert morph_play.getState() == "PLAY"