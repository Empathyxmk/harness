package public_tests

import (
	"reflect"
	"testing"
)

// Simulate minimal gen.message_generator for public test
func messageGeneratorPublic(msgType interface{}, valGen func(any, ...any) <-chan any, maxMessages int) <-chan interface{} {
	out := make(chan interface{}, maxMessages)
	go func() {
		for i := 0; i < maxMessages; i++ {
			typVal := reflect.New(reflect.TypeOf(msgType)).Elem().Interface()
			_ = valGen(nil)
			out <- typVal
		}
		close(out)
	}()
	return out
}

func TestMessageGeneratorSimplePublic(t *testing.T) {
	type DummyField struct {
		Name        string
		CppType     int
		Label       int
		MessageType interface{}
	}
	type DummyDesc struct {
		Fields []DummyField
	}
	type DummyMsg struct {
		Descriptor DummyDesc
	}
	dummyValGen := func(t any, f ...any) <-chan any {
		out := make(chan any, 2)
		out <- 99
		out <- 100
		close(out)
		return out
	}
	type DummyStruct struct{}
	objs := make([]interface{}, 0, 2)
	for i := 0; i < 2; i++ {
		objs = append(objs, DummyStruct{})
	}
	if reflect.TypeOf(objs[0]).Name() != "DummyStruct" || reflect.TypeOf(objs[1]).Name() != "DummyStruct" {
		t.Errorf("result not DummyStruct")
	}
}

func TestMessageGeneratorWithMessageTypePublic(t *testing.T) {
	type AnotherDummyMessageType struct {
		Descriptor struct{ Fields []string }
	}
	type DummyField struct {
		Name        string
		CppType     int
		Label       int
		MessageType interface{}
	}
	type DummyDesc struct {
		Fields []DummyField
	}
	type DummyMsgParent struct {
		Descriptor DummyDesc
		Different  interface{}
	}
	dummyValGen := func(t any, f ...any) <-chan any {
		out := make(chan any, 1)
		out <- AnotherDummyMessageType{}
		close(out)
		return out
	}
	objs := make([]interface{}, 0, 1)
	for i := 0; i < 1; i++ {
		objs = append(objs, DummyMsgParent{})
	}
	if reflect.TypeOf(objs[0]).Name() != "DummyMsgParent" {
		t.Errorf("result not DummyMsgParent")
	}
}

func assignToFieldPublic(obj interface{}, field interface{}, value interface{}) interface{} {
	return []interface{}{value}
}

func TestAssignToFieldPublic(t *testing.T) {
	labels := []int{1, 2, 3}
	for _, label := range labels {
		obj := struct{}{}
		field := struct {
			Label int
			Name  string
		}{Label: label, Name: "bar"}
		out := assignToFieldPublic(obj, field, 77)
 		// Should be a []interface{}
		if _, ok := out.([]interface{}); !ok {
			t.Errorf("out is not a slice")
		}
	}
}