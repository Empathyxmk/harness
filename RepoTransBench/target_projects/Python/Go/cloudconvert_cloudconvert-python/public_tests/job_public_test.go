package public_tests

import "testing"

type JobPublic struct {
	Id string
}

func TestJobDummyPublic(t *testing.T) {
	j := JobPublic{Id: "1"}
	if j.Id != "1" {
		t.Errorf("Expected Id=1, got %v", j.Id)
	}
}

func TestJobImportsPublic(t *testing.T) {
	j := JobPublic{Id: "33"}
	if j.Id == "" {
		t.Errorf("JobPublic struct should have field Id")
	}
}