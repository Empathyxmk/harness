package unit

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

func TestWorkflowProcessorPublic(t *testing.T) {
	taskObj := &TaskObj{Request: &TaskRequest{ID: "bead-feed", Retries: 2}}
	wf := new(WorkflowMock)
	wf.On("Tick").Return(false)
	wf.workflowOptions = map[string]interface{}{"extra": 99}
	wf.On("ToDict").Return(map[string]interface{}{})
	wf.On("GetRetryCountdown").Return(10)

	workflowProcessor := func(taskObj *TaskObj, data map[string]string, wf *WorkflowMock) {
		// logic ported from Python
		wf.workflowOptions = map[string]interface{}{"extra": 99}
		tick := wf.Tick()
		if !tick {
			// Not retried
		} else {
			taskObj.Request.Retries = taskObj.Request.Retries - 1
			taskObj.Called("retry", map[string]interface{}{"workflow_dict": wf.ToDict()}, wf.GetRetryCountdown())
		}
	}

	workflowProcessor(taskObj, map[string]string{"x": "y"}, wf)
	wf.AssertCalled(t, "Tick")
	wf.AssertNotCalled(t, "GetRetryCountdown")
	taskObj.AssertNotCalled(t, "retry", mock.Anything, mock.Anything)

	wf.On("Tick").Return(true)
	workflowProcessor(taskObj, map[string]string{"x": "y"}, wf)
	taskObj.AssertCalled(t, "retry", mock.Anything, mock.Anything)
	assert.Equal(t, 1, taskObj.Request.Retries)
}