package tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestDemoCoverage_Add_PositiveNumbers(t *testing.T) {
	demo := NewDemoCoverage()
	assert.Equal(t, 5, demo.Add(2, 3))
}

func TestDemoCoverage_Add_NegativeNumbers(t *testing.T) {
	demo := NewDemoCoverage()
	assert.Equal(t, -5, demo.Add(-2, -3))
}

func TestDemoCoverage_IsEven_EvenNumber(t *testing.T) {
	demo := NewDemoCoverage()
	assert.True(t, demo.IsEven(4))
}

func TestDemoCoverage_IsEven_OddNumber(t *testing.T) {
	demo := NewDemoCoverage()
	assert.False(t, demo.IsEven(5))
}

func TestDemoCoverage_Divide_RegularCase(t *testing.T) {
	demo := NewDemoCoverage()
	assert.Equal(t, 2, demo.Divide(6, 3))
}

func TestDemoCoverage_Divide_DivideByZero(t *testing.T) {
	demo := NewDemoCoverage()
	defer func() {
		if r := recover(); r != nil {
			assert.Equal(t, "/ by zero", r.(error).Error())
		} else {
			t.Fail()
		}
	}()
	demo.Divide(10, 0)
}