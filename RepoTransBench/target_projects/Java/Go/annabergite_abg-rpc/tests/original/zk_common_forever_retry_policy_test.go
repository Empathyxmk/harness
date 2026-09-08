package tests

import (
	"errors"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

type ForeverRetryPolicy struct {
	BaseSleepTime int
	MaxSleepTime  int
}

type RetrySleeper interface {
	Sleep(time.Duration) error
}

type testSleeper struct {
	interrupt bool
}

func (s *testSleeper) Sleep(d time.Duration) error {
	if s.interrupt {
		return errors.New("interrupted")
	}
	return nil
}

func NewForeverRetryPolicy(baseMs, maxMs int) (*ForeverRetryPolicy, error) {
	if baseMs < 0 || maxMs <= 0 || baseMs > maxMs {
		return nil, errors.New("illegal argument")
	}
	return &ForeverRetryPolicy{BaseSleepTime: baseMs, MaxSleepTime: maxMs}, nil
}

func (f *ForeverRetryPolicy) AllowRetry(attempt int, elapsed int, sleeper RetrySleeper) bool {
	err := sleeper.Sleep(time.Duration(f.BaseSleepTime) * time.Millisecond)
	return err == nil
}

func TestConstructorAndAllowValid(t *testing.T) {
	policy, err := NewForeverRetryPolicy(10, 100)
	assert.NotNil(t, policy)
	assert.NoError(t, err)

	sleeper := &testSleeper{}
	assert.True(t, policy.AllowRetry(0, 0, sleeper))
	assert.True(t, policy.AllowRetry(5, 0, sleeper))
	assert.True(t, policy.AllowRetry(-1, 0, sleeper))
}

func TestAllowRetryInterrupted(t *testing.T) {
	policy, _ := NewForeverRetryPolicy(10, 100)
	sleeper := &testSleeper{interrupt: true}
	assert.False(t, policy.AllowRetry(0, 0, sleeper))
}

func TestConstructorInvalidArguments(t *testing.T) {
	_, err1 := NewForeverRetryPolicy(-1, 10)
	assert.Error(t, err1)
	_, err2 := NewForeverRetryPolicy(1, 0)
	assert.Error(t, err2)
	_, err3 := NewForeverRetryPolicy(100, 10)
	assert.Error(t, err3)
}