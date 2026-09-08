package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Stubs for interface, similar pattern to the tests/original version
type AnotherDummyTest struct{}

type IRetryAnalyzer interface{}
type ITestAnnotation interface {
	GetRetryAnalyzer() IRetryAnalyzer
	SetRetryAnalyzer(impl any)
}

type FakeAnnotation struct {
	analyzer     IRetryAnalyzer
	setCalled    bool
	setArg       any
}

func (a *FakeAnnotation) GetRetryAnalyzer() IRetryAnalyzer {
	return a.analyzer
}

func (a *FakeAnnotation) SetRetryAnalyzer(impl any) {
	a.setCalled = true
	a.setArg = impl
	a.analyzer = impl
}

type RetryListener struct{}

func (rl *RetryListener) Transform(annotation ITestAnnotation, testClass any, constructor any, method any) {
	if annotation.GetRetryAnalyzer() == nil {
		annotation.SetRetryAnalyzer("TestngRetry")
	}
}

func TestTransformSetsRetryAnalyzerWhenNull(t *testing.T) {
	listener := &RetryListener{}
	fake := &FakeAnnotation{analyzer: nil}
	listener.Transform(fake, AnotherDummyTest{}, nil, nil)
	assert.True(t, fake.setCalled, "SetRetryAnalyzer should be called.")
	assert.Equal(t, "TestngRetry", fake.setArg)
}

func TestTransformDoesNotOverrideIfAlreadySet(t *testing.T) {
	listener := &RetryListener{}
	fake := &FakeAnnotation{analyzer: struct{}{}}
	listener.Transform(fake, AnotherDummyTest{}, nil, nil)
	assert.False(t, fake.setCalled, "SetRetryAnalyzer should NOT be called.")
}