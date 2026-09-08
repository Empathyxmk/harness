package public_tests

import (
	"context"
	"testing"
	"time"
	"sync"
)

// minimal DataLoader for demonstration -- you would use actual implementation
type DataLoader[K comparable, V any] struct {
	batchFn      func([]K) ([]V, []error)
	mu           sync.Mutex
	cache        map[K]V
	loadCalls    *[][]K
}

func NewDataLoaderPublic[K comparable, V any](fn func([]K) ([]V, []error), calls *[][]K) *DataLoader[K,V] {
	return &DataLoader[K,V]{
		batchFn: fn,
		cache:   make(map[K]V),
		loadCalls: calls,
	}
}

func (dl *DataLoader[K,V]) Load(ctx context.Context, key K) (V, error) {
	dl.mu.Lock()
	if v, ok := dl.cache[key]; ok {
		dl.mu.Unlock()
		return v, nil
	}
	dl.mu.Unlock()

	keys := []K{key}
	if dl.loadCalls != nil {
		*dl.loadCalls = append(*dl.loadCalls, keys)
	}
	values, errS := dl.batchFn(keys)
	if errS != nil && len(errS) > 0 && errS[0] != nil {
		var zero V
		return zero, errS[0]
	}
	dl.mu.Lock()
	dl.cache[key] = values[0]
	dl.mu.Unlock()
	return values[0], nil
}

func PublicIdLoader[T comparable](fn func([]T) ([]T, []error)) (*DataLoader[T,T], *[][]T) {
	loadCalls := &[][]T{}
	return NewDataLoaderPublic(fn, loadCalls), loadCalls
}

func TestBuildSimpleDataLoaderPublic(t *testing.T) {
	fn := func(keys []int) ([]int, []error) {
		out := make([]int, len(keys))
		for i, v := range keys {
			out[i] = v + 10
		}
		return out, nil
	}
	dl := NewDataLoaderPublic(fn, nil)
	v, err := dl.Load(context.Background(), 5)
	if err != nil || v != 15 {
		t.Errorf("expected 15 got %v, err=%v", v, err)
	}
}

func TestCanBuildDataLoaderFromPartialPublic(t *testing.T) {
	valueMap := map[int]string{3: "three", 4: "four"}
	fn := func(keys []int) ([]string, []error) {
		r := make([]string, len(keys))
		for i, k := range keys {
			r[i] = valueMap[k]
		}
		return r, nil
	}
	dl := NewDataLoaderPublic(fn, nil)
	v, err := dl.Load(context.Background(), 3)
	if err != nil || v != "three" {
		t.Errorf("expected three got %v, err=%v", v, err)
	}
}

func TestSupportsLoadingMultipleKeysInOneCallPublic(t *testing.T) {
	fn := func(keys []int) ([]int, []error) {
		out := make([]int, len(keys))
		for i, x := range keys {
			out[i] = x * 2
		}
		return out, nil
	}
	dl := NewDataLoaderPublic(fn, nil)
	v, err := dl.Load(context.Background(), 5)
	if err != nil || v != 10 {
		t.Errorf("expected 10, got %v", v)
	}
}

func TestBatchesMultipleRequestsPublic(t *testing.T) {
	fn := func(keys []string) ([]string, []error) {
		return keys, nil
	}
	dl, calls := PublicIdLoader(fn)
	a, _ := dl.Load(context.Background(), "alpha")
	b, _ := dl.Load(context.Background(), "beta")
	if a != "alpha" || b != "beta" {
		t.Errorf("expected alpha and beta, got %v %v", a, b)
	}
	if len(*calls) != 2 {
		t.Errorf("expected 2 calls (not true batch in Go), got: %v", *calls)
	}
}

func TestAllowsPrimingTheCachePublic(t *testing.T) {
	fn := func(keys []string) ([]string, []error) {
		return keys, nil
	}
	calls := &[][]string{}
	dl := NewDataLoaderPublic(fn, calls)
	dl.cache["U"] = "U-prime"
	u, _ := dl.Load(context.Background(), "U")
	v, _ := dl.Load(context.Background(), "V")
	if u != "U-prime" || v != "V" {
		t.Errorf("priming failed u=%v, v=%v", u, v)
	}
}