import pytest
from celery_dyrygent.celery import entities

def test_signature_public():
    # Use alternate values to test Signature
    sig = entities.Signature(name="test_func", args=[9, 8], kwargs={"k": 7})
    assert sig.name == "test_func"
    assert sig.args == [9, 8]
    assert sig.kwargs["k"] == 7

def test_chord_public():
    # Different header and body than existing
    header = [entities.Signature(name="sigA", args=[1])]
    body = entities.Signature(name="bodyA", args=[])
    chord = entities.Chord(header, body)
    assert chord.header[0].name == "sigA"
    assert chord.body.name == "bodyA"

def test_chain_and_group_public():
    c = entities.Chain([entities.Signature("z")])
    g = entities.Group([entities.Signature("a"), entities.Signature("b", args=[1])])
    assert len(c.tasks) == 1
    assert len(g.tasks) == 2