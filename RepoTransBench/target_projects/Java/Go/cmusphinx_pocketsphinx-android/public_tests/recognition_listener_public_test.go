package public_tests

import (
	"testing"
)

type Hypothesis struct {
	Hypstr    string
	BestScore int
}

type RecognitionListener interface {
	OnReadyForSpeech()
	OnBeginningOfSpeech()
	OnEndOfSpeech()
	OnPartialResult(hypothesis *Hypothesis)
	OnResult(hypothesis *Hypothesis)
	OnError(err error)
	OnTimeout()
}

type CallbackCounter struct {
	ready, begin, end, partial, result, error, timeout int
}

func (c *CallbackCounter) OnReadyForSpeech()               { c.ready++ }
func (c *CallbackCounter) OnBeginningOfSpeech()            { c.begin++ }
func (c *CallbackCounter) OnEndOfSpeech()                  { c.end++ }
func (c *CallbackCounter) OnPartialResult(_ *Hypothesis)   { c.partial++ }
func (c *CallbackCounter) OnResult(_ *Hypothesis)          { c.result++ }
func (c *CallbackCounter) OnError(_ error)                 { c.error++ }
func (c *CallbackCounter) OnTimeout()                      { c.timeout++ }

func TestRecognitionListenerMethodsWithDifferentData(t *testing.T) {
	cc := &CallbackCounter{}
	cc.OnReadyForSpeech()
	cc.OnReadyForSpeech()
	cc.OnBeginningOfSpeech()
	cc.OnPartialResult(&Hypothesis{"different_partial", 100})
	cc.OnEndOfSpeech()
	cc.OnEndOfSpeech()
	cc.OnResult(&Hypothesis{"different_result", 99})
	cc.OnResult(&Hypothesis{"result_again", -5})
	cc.OnError(nil)
	cc.OnError(nil)
	cc.OnTimeout()
	cc.OnTimeout()

	if cc.ready != 2 {
		t.Errorf("Expected ready=2, got %d", cc.ready)
	}
	if cc.begin != 1 {
		t.Errorf("Expected begin=1, got %d", cc.begin)
	}
	if cc.end != 2 {
		t.Errorf("Expected end=2, got %d", cc.end)
	}
	if cc.partial != 1 {
		t.Errorf("Expected partial=1, got %d", cc.partial)
	}
	if cc.result != 2 {
		t.Errorf("Expected result=2, got %d", cc.result)
	}
	if cc.error != 2 {
		t.Errorf("Expected error=2, got %d", cc.error)
	}
	if cc.timeout != 2 {
		t.Errorf("Expected timeout=2, got %d", cc.timeout)
	}
}