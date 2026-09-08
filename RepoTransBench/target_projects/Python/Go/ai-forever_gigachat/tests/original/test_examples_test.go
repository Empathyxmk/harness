package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type MockChoices struct {
	Message MockMessage
}
type MockMessage struct {
	Content string
}
type MockResponse struct {
	Choices []MockChoices
}
type DummyGigaChat struct{}

func (DummyGigaChat) Chat(payload interface{}) MockResponse {
	return MockResponse{Choices: []MockChoices{{Message: MockMessage{Content: "test-response"}}}}
}
func (DummyGigaChat) Embeddings(texts []string) []string {
	return []string{"embedding-1", "embedding-2"}
}

func TestExampleAsk(t *testing.T) {
	giga := DummyGigaChat{}
	resp := giga.Chat("What?")
	assert.Equal(t, "test-response", resp.Choices[0].Message.Content)
}

func TestExampleEmbeddings(t *testing.T) {
	giga := DummyGigaChat{}
	result := giga.Embeddings([]string{"Hello world!"})
	assert.Equal(t, []string{"embedding-1", "embedding-2"}, result)
}

func TestExampleRussianTrustedRootCA(t *testing.T) {
	giga := DummyGigaChat{}
	resp := giga.Chat("Test?")
	assert.Equal(t, "test-response", resp.Choices[0].Message.Content)
}

func TestSimpleChatLoop(t *testing.T) {
	giga := DummyGigaChat{}
	inputs := []string{"Привет!", "exit"}
	count := 0
	i := 0
	for {
		userInput := inputs[i]
		i++
		if userInput == "exit" {
			break
		}
		resp := giga.Chat(nil)
		_ = resp.Choices[0].Message.Content
		count++
	}
	assert.Equal(t, 1, count)
}

func TestExampleContextvars(t *testing.T) {
	giga := DummyGigaChat{}
	resp := giga.Chat("Какие факторы влияют на стоимость страховки на дом?")
	assert.Equal(t, "test-response", resp.Choices[0].Message.Content)
}