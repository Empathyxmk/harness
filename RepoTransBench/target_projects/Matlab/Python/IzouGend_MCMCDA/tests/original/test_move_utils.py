import pytest
import numpy as np
from src.izougend_mcmcda.move_utils import move3_split, move7_track_update

def mock_move1_birth(W):
    # Simple mock: return initial W, mark flag
    Out = W.copy()
    Out['mock_called'] = True
    return Out

def test_move3_split_case1_no_long_tracks():
    # All tracks < 4 frames
    W = {
        'track': [
            {'tau': [{'frame': 1, 'y': 1}, {'frame': 2, 'y': 2}, {'frame': 3, 'y': 3}]},
            {'tau': [{'frame': 1, 'y': 1}]},
        ],
        'tracks': 2
    }
    Out = move3_split(W, 3, 3, 2, 3)
    assert Out == 666

def test_move3_split_case2_successful_split():
    # One track with >= 4 frames
    W = {
        'track': [
            {'tau': [
                {'frame': 1, 'y': 10},
                {'frame': 2, 'y': 20},
                {'frame': 3, 'y': 30},
                {'frame': 4, 'y': 40},
                {'frame': 5, 'y': 50, 'islast': 1}
            ]}
        ],
        'tracks': 1
    }
    Out = move3_split(W, 5, 5, 1, 5)
    assert isinstance(Out, dict)
    assert Out['tracks'] == 2
    assert ('islast' in Out['track'][0]['tau'][-1] or 'islast' in Out['track'][0]['tau'][0])

def test_move7_track_update_case1_all_dead():
    # All tracks are dead
    W = {'track': [{'tau': [{'frame': None}]}], 'tracks': 1}
    Out = move7_track_update(W, 5, 5, 1, 5, [], [], move1_birth=mock_move1_birth)
    assert Out == 666

def test_move7_track_update_case2_success():
    # One track with alive frames
    W = {
        'track': [
            {'tau': [
                {'frame': 1, 'y': 10},
                {'frame': 2, 'y': 20},
                {'frame': 3, 'y': 30},
                {'frame': 4, 'y': 40, 'islast': 1}
            ]}
        ],
        'tracks': 1
    }
    Out = move7_track_update(W, 4, 4, 1, 4, [], [], move1_birth=mock_move1_birth)
    assert isinstance(Out, dict)
    assert Out.get('mock_called', False) is True
    assert Out['track'][0]['tau'][0]['AAA'] == "mossa7"