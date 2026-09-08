package original

import (
	"testing"
)

// Minimal Hypothesis and RecognitionListener definitions for test
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

func TestRecognitionListenerMethods(t *testing.T) {
	cc := &CallbackCounter{}
	cc.OnReadyForSpeech()
	cc.OnBeginningOfSpeech()
	cc.OnEndOfSpeech()
	cc.OnPartialResult(&Hypothesis{"foo", 10})
	cc.OnResult(&Hypothesis{"bar", 9})
	cc.OnError(nil)
	cc.OnTimeout()

	if cc.ready != 1 {
		t.Errorf("Expected ready=1, got %d", cc.ready)
	}
	if cc.begin != 1 {
		t.Errorf("Expected begin=1, got %d", cc.begin)
	}
	if cc.end != 1 {
		t.Errorf("Expected end=1, got %d", cc.end)
	}
	if cc.partial != 1 {
		t.Errorf("Expected partial=1, got %d", cc.partial)
	}
	if cc.result != 1 {
		t.Errorf("Expected result=1, got %d", cc.result)
	}
	if cc.error != 1 {
		t.Errorf("Expected error=1, got %d", cc.error)
	}
	if cc.timeout != 1 {
		t.Errorf("Expected timeout=1, got %d", cc.timeout)
	}
}