import pytest
from src.corpus import Corpus

def test_corpus_basic_properties_and_mutations():
    # Test construction
    corpus = Corpus()
    assert corpus.USE_SPELLING is False

    # Test default sizes are zero
    assert corpus.nsentences == 0
    assert corpus.nwords == 0
    assert corpus.nactions == 0
    assert corpus.npos == 0
    assert corpus.nsentencestest == 0

    # Test inserting into maps and their retrieval
    corpus.nsentences = 2
    corpus.nwords = 5
    corpus.nactions = 3
    corpus.npos = 4
    corpus.nsentencestest = 1

    corpus.sentences[0] = [1, 2, 3]
    corpus.sentences[1] = [4, 5, 6]

    corpus.sentencesPos[0] = [10, 11, 12]

    corpus.correct_act_sent[0] = [100]
    corpus.correct_act_sentDev[0] = [200]
    corpus.sentencesDev[0] = [7, 8]
    corpus.sentencesPosDev[0] = [13, 14]
    corpus.sentencesStrDev[0] = ["the", "cat"]
    corpus.nsentencesDev = 1

    # Check map access
    assert corpus.sentences[0][0] == 1
    assert corpus.sentences[1][2] == 6
    assert corpus.sentencesPos[0][2] == 12
    assert corpus.correct_act_sent[0][0] == 100
    assert corpus.correct_act_sentDev[0][0] == 200
    assert corpus.sentencesDev[0][1] == 8
    assert corpus.sentencesPosDev[0][1] == 14
    assert corpus.sentencesStrDev[0][1] == "cat"
    assert corpus.nsentencesDev == 1

    # Modify and check bool flag
    corpus.USE_SPELLING = True
    assert corpus.USE_SPELLING

    # Erase and check removal from maps
    corpus.sentences.pop(0)
    assert 0 not in corpus.sentences