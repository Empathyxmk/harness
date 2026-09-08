package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Assistant struct{}
type AssistantDelete struct{}
type AssistantFileDelete struct{}
type Assistants struct {
	Data []Assistant
}
type CreateAssistant struct {
	AssistantID string
}

type AssistantClient struct{}

func (c *AssistantClient) Get() Assistants {
	return Assistants{Data: []Assistant{{}, {}}}
}
func (c *AssistantClient) Create(model, name, instructions string) CreateAssistant {
	return CreateAssistant{AssistantID: "111"}
}
func (c *AssistantClient) Update(assistantID string) Assistant {
	return Assistant{}
}
func (c *AssistantClient) DeleteFile(assistantID, fileID string) AssistantFileDelete {
	return AssistantFileDelete{}
}
func (c *AssistantClient) Delete(assistantID string) AssistantDelete {
	return AssistantDelete{}
}

func newAssistantClient() *AssistantClient { return &AssistantClient{} }

func TestGetAssistants(t *testing.T) {
	client := newAssistantClient()
	resp := client.Get()
	assert.Len(t, resp.Data, 2)
}

func TestPostAssistants(t *testing.T) {
	client := newAssistantClient()
	resp := client.Create("GigaChat", "name", "123")
	assert.Equal(t, "111", resp.AssistantID)
}

func TestPostAssistantModify(t *testing.T) {
	client := newAssistantClient()
	resp := client.Update("111")
	assert.IsType(t, Assistant{}, resp)
}

func TestPostAssistantFilesDelete(t *testing.T) {
	client := newAssistantClient()
	resp := client.DeleteFile("111", "222")
	assert.IsType(t, AssistantFileDelete{}, resp)
}

func TestPostAssistantDelete(t *testing.T) {
	client := newAssistantClient()
	resp := client.Delete("111")
	assert.IsType(t, AssistantDelete{}, resp)
}