package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type ThreadCompletion struct{}
type ThreadCompletionChunk struct{}
type ThreadMessages struct {
	Messages []string
}
type ThreadMessagesResponse struct{}
type ThreadRunOptions struct {
	Temperature float64
}
type ThreadRunResponse struct{}
type ThreadRunResult struct {
	Messages []string
}
type Threads struct {
	Threads []string
}

type ThreadsClient struct{}

func (c *ThreadsClient) List() Threads {
	return Threads{Threads: []string{"a", "b", "c"}}
}
func (c *ThreadsClient) Retrieve(ids []string) Threads {
	return Threads{Threads: []string{"only-one"}}
}
func (c *ThreadsClient) GetMessages(threadID string) ThreadMessages {
	return ThreadMessages{Messages: []string{"msg1", "msg2"}}
}
func (c *ThreadsClient) GetRun(threadID string) ThreadRunResult {
	return ThreadRunResult{Messages: []string{"a", "b"}}
}
func (c *ThreadsClient) Delete(threadID string) bool {
	return true
}

func newThreadsClient() *ThreadsClient { return &ThreadsClient{} }

func TestGetThreads(t *testing.T) {
	c := newThreadsClient()
	resp := c.List()
	assert.Len(t, resp.Threads, 3)
}

func TestPostThreadsRetrieve(t *testing.T) {
	c := newThreadsClient()
	resp := c.Retrieve([]string{})
	assert.Len(t, resp.Threads, 1)
}

func TestGetThreadsMessages(t *testing.T) {
	c := newThreadsClient()
	resp := c.GetMessages("111")
	assert.Len(t, resp.Messages, 2)
}

func TestGetThreadsRun(t *testing.T) {
	c := newThreadsClient()
	resp := c.GetRun("111")
	assert.Len(t, resp.Messages, 2)
}

func TestPostThreadsDelete(t *testing.T) {
	c := newThreadsClient()
	resp := c.Delete("111")
	assert.True(t, resp)
}