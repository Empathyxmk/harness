package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"github.com/socialwifi_routeros_api/routeros_api"
	"github.com/socialwifi_routeros_api/routeros_api/exceptions"
)

// Mock for base connection, with methods for receive_sentence and send_sentence
type MockBase struct {
	mock.Mock
	recvIndex int
	// Return a list of sentences for ReceiveSentence, either .return_value or .side_effect
	SentencesReturn     [][]byte   // For static .return_value
	SentencesSideEffect [][][]byte // For .side_effect: list of lists
}

func (m *MockBase) ReceiveSentence() []byte {
	if len(m.SentencesSideEffect) > 0 && m.recvIndex < len(m.SentencesSideEffect) {
		val := m.SentencesSideEffect[m.recvIndex]
		m.recvIndex++
		return flatten(val)
	}
	if len(m.SentencesReturn) > 0 {
		return flatten(m.SentencesReturn)
	}
	return nil
}
func flatten(in [][]byte) []byte {
	res := []byte{}
	for _, b := range in {
		res = append(res, b...)
	}
	return res
}
func (m *MockBase) SendSentence(sentence [][]byte) {
	m.Called(sentence)
}

// Placeholder for Promise
type DummyPromise struct {
	Response interface{}
	Err      error
}

func (p *DummyPromise) Get() (interface{}, error) {
	return p.Response, p.Err
}

func TestCommunicator_LoginCall(t *testing.T) {
	// Simulates .return_value = [b'!done', b'=ret=some-hex', b'.tag=1']
	base := &MockBase{}
	base.SentencesReturn = [][]byte{[]byte("!done"), []byte("=ret=some-hex"), []byte(".tag=1")}
	communicator := routeros_api.NewApiCommunicator(base)
	promise := communicator.Call("/", "login")
	response, err := promise.Get()
	assert.NoError(t, err)
	// Response is expected to have DoneMessage map/field with "ret"
	if asMap, ok := response.(map[string][]byte); ok {
		assert.Equal(t, []byte("some-hex"), asMap["ret"])
	} else {
		t.Errorf("Response did not have expected type, got %T", response)
	}
}

func TestCommunicator_NormalCall(t *testing.T) {
	base := &MockBase{}
	base.SentencesSideEffect = [][][]byte{
		{[]byte("!re"), []byte("=x=y"), []byte(".tag=1")},
		{[]byte("!done"), []byte(".tag=1")},
	}
	communicator := routeros_api.NewApiCommunicator(base)
	promise := communicator.Call("/interface/", "print")
	response, err := promise.Get()
	assert.NoError(t, err)
	expected := []map[string][]byte{{"x": []byte("y")}}
	assert.Equal(t, expected, response)
}

func TestCommunicator_MixedCalls(t *testing.T) {
	base := &MockBase{}
	base.SentencesSideEffect = [][][]byte{
		{[]byte("!re"), []byte("=x1=y1"), []byte(".tag=1")},
		{[]byte("!re"), []byte("=x2=y2"), []byte(".tag=2")},
		{[]byte("!done"), []byte(".tag=1")},
		{[]byte("!done"), []byte(".tag=2")},
	}
	communicator := routeros_api.NewApiCommunicator(base)
	promise := communicator.Call("/interface/", "print")
	response2, _ := communicator.Call("/interface/", "print").Get()
	response1, _ := promise.Get()
	expected1 := []map[string][]byte{{"x1": []byte("y1")}}
	expected2 := []map[string][]byte{{"x2": []byte("y2")}}
	assert.Equal(t, expected1, response1)
	assert.Equal(t, expected2, response2)
}

func TestCommunicator_ErrorCall(t *testing.T) {
	base := &MockBase{}
	base.SentencesSideEffect = [][][]byte{
		{[]byte("!trap"), []byte("=message=y"), []byte(".tag=1")},
		{[]byte("!done"), []byte(".tag=1")},
	}
	communicator := routeros_api.NewApiCommunicator(base)
	promise := communicator.Call("/file/", "print")
	_, err := promise.Get()
	assert.ErrorIs(t, err, exceptions.RouterOsApiCommunicationError)
}

func TestCommunicator_EmptyCall(t *testing.T) {
	base := &MockBase{}
	base.SentencesSideEffect = [][][]byte{
		{[]byte("!empty"), []byte(".tag=1")},
		{[]byte("!done"), []byte(".tag=1")},
	}
	communicator := routeros_api.NewApiCommunicator(base)
	promise := communicator.Call("/file/", "print")
	response, err := promise.Get()
	assert.NoError(t, err)
	assert.Equal(t, []interface{}{}, response)
}

func TestCommunicator_QueryCall(t *testing.T) {
	base := &MockBase{}
	base.SentencesReturn = [][]byte{[]byte("!done"), []byte(".tag=1")}
	communicator := routeros_api.NewApiCommunicator(base)
	promise := communicator.Call("/interface/", "print", map[string]string{"x": "y"}, nil)
	_, err := promise.Get()
	assert.NoError(t, err)
	base.AssertCalled(t, "SendSentence", [][]byte{[]byte("/interface/print"), []byte("?x=y"), []byte(".tag=1")})
}

func TestCommunicator_SetCall(t *testing.T) {
	base := &MockBase{}
	base.SentencesReturn = [][]byte{[]byte("!done"), []byte(".tag=1")}
	communicator := routeros_api.NewApiCommunicator(base)
	communicator.Call("/interface/", "set", map[string][]byte{"x": []byte("y")}, nil)
	base.AssertCalled(t, "SendSentence", [][]byte{[]byte("/interface/set"), []byte("=x=y"), []byte(".tag=1")})
}

func TestCommunicator_CallWithArguments(t *testing.T) {
	base := &MockBase{}
	base.SentencesReturn = [][]byte{[]byte("!done"), []byte(".tag=1")}
	communicator := routeros_api.NewApiCommunicator(base)
	communicator.Call("/interface/monitor-traffic/", "monitor", map[string]string{"interface": "ether1"}, nil)
	base.AssertCalled(t, "SendSentence", [][]byte{[]byte("/interface/monitor-traffic/monitor"), []byte("=interface=ether1"), []byte(".tag=1")})
}

func TestCommunicator_CallWithoutArguments(t *testing.T) {
	base := &MockBase{}
	base.SentencesReturn = [][]byte{[]byte("!done"), []byte(".tag=1")}
	communicator := routeros_api.NewApiCommunicator(base)
	communicator.Call("/interface/monitor-traffic/", "monitor", map[string]interface{}{"once": nil}, nil)
	base.AssertCalled(t, "SendSentence", [][]byte{[]byte("/interface/monitor-traffic/monitor"), []byte("=once"), []byte(".tag=1")})
}

func TestCommunicator_AsyncErrorRaisesWhenSynchronizing(t *testing.T) {
	base := &MockBase{}
	base.SentencesSideEffect = [][][]byte{
		{[]byte("!trap"), []byte("=message=m"), []byte(".tag=1")},
		{[]byte("!done"), []byte(".tag=2")},
		{[]byte("!done"), []byte(".tag=1")},
	}
	communicator := routeros_api.NewApiCommunicator(base)
	promise := communicator.Call("/interface/", "print")
	_, _ = communicator.Call("/interface/", "print").Get()
	_, err := promise.Get()
	assert.ErrorIs(t, err, exceptions.RouterOsApiCommunicationError)
}