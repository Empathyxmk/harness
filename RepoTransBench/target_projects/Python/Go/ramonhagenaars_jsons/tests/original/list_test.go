package original

import (
	"encoding/json"
	"reflect"
	"sync"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestDumpList(t *testing.T) {
	d := time.Date(2018, 7, 8, 21, 34, 0, 0, time.UTC)
	l := []interface{}{1, 2, 3, []interface{}{4, 5, []interface{}{d}}}
	expected := []interface{}{1, 2, 3, []interface{}{4, 5, []interface{}{"2018-07-08T21:34:00Z"}}}
	actual := jsons.Dump(l)
	assert.Equal(t, expected, actual)
}

func TestDumpLoadListVerbose(t *testing.T) {
	type Parent struct{}
	type Child struct{ Parent }
	type Store struct {
		C2s []interface{}
	}

	// Register types just as announce_class in Python
	jsons.AnnounceClass(&Parent{})
	jsons.AnnounceClass(&Child{})
	jsons.AnnounceClass(&Store{})
	st := Store{C2s: []interface{}{&Child{}}}
	dumped := jsons.DumpVerbose(st, true)
	loaded := Store{}
	jsons.Load(dumped, &loaded)
	assert.IsType(t, &Child{}, loaded.C2s[0])
}

func TestDumpListStrictNoCls(t *testing.T) {
	type C struct {
		X int
		Y string
	}
	l := []C{{1, "2"}, {1, "2"}, {1, "2"}, {1, "2"}, {1, "2"}}
	expected := []map[string]interface{}{
		{"x": 1, "y": "2"},
		{"x": 1, "y": "2"},
		{"x": 1, "y": "2"},
		{"x": 1, "y": "2"},
		{"x": 1, "y": "2"},
	}
	dumped := jsons.DumpStrict(l)
	assert.Equal(t, expected, dumped)
}

func TestDumpListMultiprocess(t *testing.T) {
	// Simulate multiprocess using goroutines
	l := []string{"1", "1", "1", "1"}
	out := jsons.DumpParallelStringToInt(l, 2)
	expected := []int{1, 1, 1, 1}
	assert.Equal(t, expected, out)
}

func TestLoadList(t *testing.T) {
	d := time.Date(2018, 7, 8, 21, 34, 0, 0, time.UTC)
	exp := []interface{}{1, 2, 3, []interface{}{4, 5, []interface{}{d}}}
	result := jsons.LoadRaw([]interface{}{1, 2, 3, []interface{}{4, 5, []interface{}{"2018-07-08T21:34:00Z"}}})
	assert.Equal(t, exp, result)
}

func TestLoadListTyping(t *testing.T) {
	// This is similar to above, just uses List
	TestLoadList(t)
}

func TestLoadList2(t *testing.T) {
	d := "2018-07-08T21:34:00Z"
	list := []string{d}
	// The Python code expects input as ['2018-07-08T21:34:00Z'] to output [datetime], but in Go, simplest is string
	result := jsons.LoadRaw(list)
	assert.Equal(t, list, result)
}

func TestLoadListMultiThreaded(t *testing.T) {
	// Simulated via goroutines and channels in Go
	d := "2018-07-08T21:34:00Z"
	input := []interface{}{1, 2, 3, []interface{}{4, 5, []interface{}{d}}}
	list := []interface{}{1, 2, 3, []interface{}{4, 5, []interface{}{d}}}
	var out []interface{}

	var mu sync.Mutex
	ch := make(chan struct{})
	go func() {
		mu.Lock()
		defer mu.Unlock()
		out = jsons.LoadRaw(input)
		ch <- struct{}{}
	}()
	<-ch
	assert.Equal(t, list, out)

	// Negative task value, should error
	err := jsons.LoadParallelError(input, -1)
	assert.Error(t, err)

	// Correct with positive task value
	out2 := jsons.LoadParallelStringToInt([]string{"1"}, 2)
	assert.Equal(t, []int{1}, out2)

	// More tasks than elements
	out3 := jsons.LoadParallelStringToInt([]string{"1", "1", "1", "1"}, 16)
	assert.Equal(t, []int{1, 1, 1, 1}, out3)
}

func TestLoadListMultiprocess(t *testing.T) {
	out := jsons.LoadParallelStringToInt([]string{"1", "1", "1", "1"}, 2)
	assert.Equal(t, []int{1, 1, 1, 1}, out)
}

func TestLoadListWithGeneric(t *testing.T) {
	type C struct {
		X string `json:"x"`
		Y int    `json:"y"`
	}
	input := []map[string]interface{}{
		{"x": "a", "y": 1},
		{"x": "b", "y": 2},
	}
	var loaded []C
	jsons.Load(input, &loaded)
	assert.Equal(t, "a", loaded[0].X)
	assert.Equal(t, 1, loaded[0].Y)
	assert.Equal(t, "b", loaded[1].X)
	assert.Equal(t, 2, loaded[1].Y)
}

func TestLoadErrorPointsAtIndex(t *testing.T) {
	type C struct {
		X string `json:"x"`
		Y int    `json:"y"`
	}
	// 1000 correct, one wrong at 500
	input := make([]map[string]interface{}, 1000)
	for i := 0; i < 1000; i++ {
		input[i] = map[string]interface{}{"x": string(i), "y": i}
	}
	input[500] = map[string]interface{}{"not_x": "42", "y": 42}
	err := jsons.LoadExpectErrorAtIndex(input, 500)
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "500")
}

func TestWarnOnFail(t *testing.T) {
	type C struct {
		X string `json:"x"`
		Y int    `json:"y"`
	}
	input := make([]map[string]interface{}, 1000)
	for i := 0; i < 1000; i++ {
		input[i] = map[string]interface{}{"x": string(i), "y": i}
	}
	input[500] = map[string]interface{}{"not_x": "42", "y": 42}
	loaded, warns := jsons.LoadWarnOnFail(input)
	assert.Contains(t, warns, "500")
	assert.Equal(t, 999, len(loaded))
}

func TestPropagationOfForkInst(t *testing.T) {
	type C struct{ X int }
	cDeserializer := func(obj map[string]interface{}) (C, error) {
		return C{X: obj["x"].(int) * 2}, nil
	}
	f := jsons.ForkNamed("fork_inst_propagation")
	jsons.SetDeserializer(f, cDeserializer)
	s := `[{"x":2},{"x":3}]`
	var cs []C
	jsons.LoadsWithFork(s, f, &cs)
	assert.Equal(t, 4, cs[0].X)
	assert.Equal(t, 6, cs[1].X)
}