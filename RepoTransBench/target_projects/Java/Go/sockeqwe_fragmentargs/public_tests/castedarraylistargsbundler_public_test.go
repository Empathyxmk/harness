package public_tests

import (
	"reflect"
	"testing"
)

type MyParcelablePublic struct {
	Str string
}

type FakeBundlePublic struct {
	arrayList interface{}
}

func (b *FakeBundlePublic) PutParcelableArrayList(key string, value interface{}) {
	b.arrayList = value
}
func (b *FakeBundlePublic) GetParcelableArrayList(key string) interface{} {
	return b.arrayList
}

type CastedArrayListArgsBundlerPublic struct{}

func (c *CastedArrayListArgsBundlerPublic) Put(key string, value interface{}, bundle *FakeBundlePublic) {
	arr, ok := value.([]MyParcelablePublic)
	if !ok {
		panic("ClassCastException")
	}
	bundle.PutParcelableArrayList(key, arr)
}

func (c *CastedArrayListArgsBundlerPublic) Get(key string, bundle *FakeBundlePublic) []MyParcelablePublic {
	arr, _ := bundle.GetParcelableArrayList(key).([]MyParcelablePublic)
	return arr
}

func TestCastedArrayListArgsBundlerWithParcelablePublicVariant(t *testing.T) {
	bundler := &CastedArrayListArgsBundlerPublic{}
	data := []MyParcelablePublic{
		{Str: "dragonfruit"},
		{Str: "peach"},
		{Str: "plum"},
	}
	bundle := &FakeBundlePublic{}
	bundler.Put("UniqueFruitKey", data, bundle)
	restored := bundler.Get("UniqueFruitKey", bundle)
	if !reflect.DeepEqual(data, restored) {
		t.Errorf("expected %v, got %v", data, restored)
	}
}