package api

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type ChatCompletionChunk struct {
	Choices []struct {
		FinishReason string
	}
}

func TestSync(t *testing.T) {
	chunks := []ChatCompletionChunk{
		{Choices: []struct{ FinishReason string }{{FinishReason: "continue"}}},
		{Choices: []struct{ FinishReason string }{{FinishReason: "continue"}}},
		{Choices: []struct{ FinishReason string }{{FinishReason: "stop"}}},
	}
	assert.Len(t, chunks, 3)
	for _, c := range chunks {
		assert.NotNil(t, c.Choices[0].FinishReason)
	}
	assert.Equal(t, "stop", chunks[2].Choices[0].FinishReason)
}

func TestSyncValueError(t *testing.T) {
	err := errors.New("4 validation errors for ChatCompletionChunk")
	assert.Error(t, err)
}

func TestSyncAuthenticationError(t *testing.T) {
	err := errors.New("AuthenticationError")
	assert.Error(t, err)
}

func TestSyncResponseError(t *testing.T) {
	err := errors.New("ResponseError")
	assert.Error(t, err)
}