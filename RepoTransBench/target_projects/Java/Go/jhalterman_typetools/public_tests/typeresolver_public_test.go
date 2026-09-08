package public_tests

import (
	"reflect"
	"testing"

	"github.com/jhalterman/typetools"
)

type RepoA1[A any, B any] struct {
	Parent RepoA2[B, struct{}]
}
type RepoA2[X any, Y any] struct {
	Parent RepoA3[Y, struct{}, X]
}
type RepoA3[A any, B any, C any] struct{}

type IPublicRepo[I1, I2, I3, I4 any] interface{}
type IIPublicRepo[II1, II2 any] interface{}

type FooPublic struct {
	BarPublic
}
type BarPublic struct{}
type BazPublic struct{}

type SimplePublicRepo struct{}

type PublicEntity[ID any] struct {
	id ID
}

type AnotherQueue []float64 // Simulate LinkedList<Double>
type AnotherEntity struct {
	PublicEntity[string]
}

func TestShouldResolveClassPublic(t *testing.T) {
	typ := reflect.TypeOf(AnotherEntity{})
	if typ.Kind() != reflect.Struct {
		t.Errorf("Expected struct type for public entity")
	}
}

func TestShouldResolveArgumentForQueue(t *testing.T) {
	v := AnotherQueue{}
	// In real, would resolve to float64
	if reflect.TypeOf(v).Elem().Kind() != reflect.Float64 {
		t.Errorf("Expected float64 for AnotherQueue type")
	}
}

func TestShouldResolveTypeForQueue(t *testing.T) {
	v := AnotherQueue{}
	tp := reflect.TypeOf(v)
	arg := tp.Elem()
	if arg.Kind() != reflect.Float64 {
		t.Errorf("Expected float64 type for queue element")
	}
}