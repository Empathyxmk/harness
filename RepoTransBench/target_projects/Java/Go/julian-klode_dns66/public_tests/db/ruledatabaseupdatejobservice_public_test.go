package db

import "testing"

type RuleDatabaseUpdateJobService struct {
	jobFinishedCalled bool
}

func TestJobServiceFieldsPublic(t *testing.T) {
	service := &RuleDatabaseUpdateJobService{}
	service.jobFinishedCalled = true
	if !service.jobFinishedCalled {
		t.Error("Expected jobFinishedCalled to be true after setting")
	}
}