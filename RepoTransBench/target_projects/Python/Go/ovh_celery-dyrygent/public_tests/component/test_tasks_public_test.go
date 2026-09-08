package component

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type TaskObj struct {
	mock.Mock
	Request *TaskRequest
}

type TaskRequest struct {
	ID      string
	Retries int
}

type WorkflowMock struct {
	mock.Mock
	workflowOptions map[string]interface{}
	tickReturn      bool
	countdown       int
}

func (w *WorkflowMock) Tick() bool {
	args := w.Called()
	return args.Bool(0)
}

func (w *WorkflowMock) ToDict() map[string]interface{} {
	args := w.Called()
	return args.Get(0).(map[string]interface{})
}

func (w *WorkflowMock) GetRetryCountdown() int {
	args := w.Called()
	return args.Int(0)
}

func TestWorkflowProcessorWithDifferentIDs(t *testing.T) {
	taskObj := &TaskObj{Request: &TaskRequest{ID: "feed-face", Retries: 4}}
	wf := new(WorkflowMock)
	wf.On("Tick").Return(false)
	wf.workflowOptions = map[string]interface{}{}
	wf.On("ToDict").Return(map[string]interface{}{})
	wf.On("GetRetryCountdown").Return(123)

	workflowProcessor := func(taskObj *TaskObj, data map[string]string, wf *WorkflowMock) {
		tick := wf.Tick()
		if !tick {
			// Not retried
		} else {
			taskObj.Request.Retries = taskObj.Request.Retries - 1
			taskObj.Called("retry", map[string]interface{}{"workflow_dict": wf.ToDict()}, wf.GetRetryCountdown())
		}
	}

	workflowProcessor(taskObj, map[string]string{"foo": "bar"}, wf)
	wf.AssertCalled(t, "Tick")
	wf.AssertNotCalled(t, "GetRetryCountdown")
	taskObj.AssertNotCalled(t, "retry", mock.Anything, mock.Anything)

	wf.On("Tick").Return(true)
	wf.On("GetRetryCountdown").Return(10)
	workflowProcessor(taskObj, map[string]string{"foo": "bar"}, wf)
	taskObj.AssertCalled(t, "retry", mock.Anything, mock.Anything)
	assert.Equal(t, 3, taskObj.Request.Retries)
}