package public_tests

import "testing"

type CloudConvertExceptionPublic struct {
	Msg string
}
func (e CloudConvertExceptionPublic) Error() string { return e.Msg }

func TestImportExceptionsPublic(t *testing.T) {
	e := CloudConvertExceptionPublic{"public"}
	if e.Error() != "public" {
		t.Errorf("CloudConvertExceptionPublic error should contain public, got %v", e.Error())
	}
}

func TestInheritanceCloudConvertExceptionPublic(t *testing.T) {
	type SubCloudConvertException struct{ CloudConvertExceptionPublic }
	e := SubCloudConvertException{CloudConvertExceptionPublic{"public error"}}
	if _, ok := interface{}(e).(CloudConvertExceptionPublic); !ok {
		t.Errorf("SubCloudConvertException should be instance of CloudConvertExceptionPublic")
	}
	if e.Error() != "public error" {
		t.Errorf("Expected error to contain 'public error', got %v", e.Error())
	}
}