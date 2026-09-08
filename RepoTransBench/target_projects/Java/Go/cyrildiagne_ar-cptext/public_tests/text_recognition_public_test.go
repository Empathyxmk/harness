package public_tests

import (
	"errors"
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

type TextRecognition struct{}

func (tr *TextRecognition) degreesToFirebaseRotation(degrees int) (int, error) {
	switch degrees {
	case 0:
		return 0, nil
	case 90:
		return 1, nil
	case 180:
		return 2, nil
	case 270:
		return 3, nil
	default:
		return 0, errors.New("IllegalArgumentException")
	}
}

func TestDegreesToFirebaseRotationValidPublic(t *testing.T) {
	tr := &TextRecognition{}
	method := reflect.ValueOf(tr).MethodByName("degreesToFirebaseRotation")
	invoke := func(x int) int {
		results := method.Call([]reflect.Value{reflect.ValueOf(x)})
		val := int(results[0].Int())
		errif := results[1].Interface()
		assert.Equal(t, nil, errif)
		return val
	}
	assert.Equal(t, 0, invoke(0))
	assert.Equal(t, 1, invoke(90))
	assert.Equal(t, 2, invoke(180))
	assert.Equal(t, 3, invoke(270))
}

func TestDegreesToFirebaseRotationInvalidPublic(t *testing.T) {
	tr := &TextRecognition{}
	method := reflect.ValueOf(tr).MethodByName("degreesToFirebaseRotation")
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("Expected error but did not panic or return error")
		}
	}()
	results := method.Call([]reflect.Value{reflect.ValueOf(135)})
	errIf := results[1].Interface()
	if errIf == nil {
		t.Fatalf("Expected error, got nil")
	}
}