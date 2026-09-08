import pytest
from src.corpus import Corpus

def test_corpus_public_varied_data():
    # Test construction with different data
    corpus = Corpus()
    assert corpus.USE_SPELLING is False

    # Test default sizes (ensure initial values are still zero)
    assert corpus.nsentences == 0
    assert corpus.nwords == 0
    assert corpus.nactions == 0
    assert corpus.npos == 0
    assert corpus.nsentencestest == 0

    # Use different sizes from the private test
    corpus.nsentences = 5
    corpus.nwords = 8
    corpus.nactions = 2
    corpus.npos = 3
    corpus.nsentencestest = 2

    # Different sentence data
    corpus.sentences[1] = [10, 20]
    corpus.sentences[2] = [30, 40, 50]

    corpus.sentencesPos[1] = [21, 22]

    corpus.correct_act_sent[1] = [150, 151]
    corpus.correct_act_sentDev[1] = [250, 251]
    corpus.sentencesDev[1] = [17, 18, 19]
    corpus.sentencesPosDev[1] = [23, 24, 25]
    corpus.sentencesStrDev[1] = ["quick", "brown", "fox"]
    corpus.nsentencesDev = 3

    # Check map access with above different data
    assert corpus.sentences[1][1] == 20
    assert corpus.sentences[2][2] == 50
    assert corpus.sentencesPos[1][1] == 22
    assert corpus.correct_act_sent[1][0] == 150
    assert corpus.correct_act_sent[1][1] == 151
    assert corpus.correct_act_sentDev[1][1] == 251
    assert corpus.sentencesDev[1][2] == 19
    assert corpus.sentencesPosDev[1][2] == 25
    assert corpus.sentencesStrDev[1][2] == "fox"
    assert corpus.nsentencesDev == 3

    # Modify and check bool flag
    corpus.USE_SPELLING = True
    assert corpus.USE_SPELLING

    # Erase and check removal from maps (now erase key 1, not key 0!)
    corpus.sentences.pop(1)
    assert 1 not in corpus.sentences