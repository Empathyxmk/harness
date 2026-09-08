package original

import (
	"reflect"
	"testing"
)

type DummyParcelable struct{}

type FakeBundle struct {
	arrayList interface{}
}

func (b *FakeBundle) PutParcelableArrayList(key string, value interface{}) {
	b.arrayList = value
}
func (b *FakeBundle) GetParcelableArrayList(key string) interface{} {
	return b.arrayList
}

type CastedArrayListArgsBundler struct{}

func (c *CastedArrayListArgsBundler) Put(key string, value interface{}, bundle *FakeBundle) {
	arr, ok := value.([]DummyParcelable)
	if !ok {
		panic("ClassCastException")
	}
	bundle.PutParcelableArrayList(key, arr)
}

func (c *CastedArrayListArgsBundler) Get(key string, bundle *FakeBundle) []DummyParcelable {
	arr, _ := bundle.GetParcelableArrayList(key).([]DummyParcelable)
	return arr
}

func TestPutThrowsIfNotArrayList(t *testing.T) {
	bundler := &CastedArrayListArgsBundler{}
	defer func() {
		if r := recover(); r == nil {
			t.Error("Expected panic (ClassCastException), but code did not panic")
		}
	}()
	bundler.Put("key", "not a slice", &FakeBundle{})
}

func TestPutAndGetWithArrayList(t *testing.T) {
	bundler := &CastedArrayListArgsBundler{}
	arrList := []DummyParcelable{{}, {}}
	bundle := &FakeBundle{}
	bundler.Put("key", arrList, bundle)

	result := bundler.Get("key", bundle)
	if !reflect.DeepEqual(arrList, result) {
		t.Errorf("Expected %v, got %v", arrList, result)
	}
}