package public_tests

import (
	"bytes"
	"encoding/json"
	"errors"
	"io"
	"os"
	"testing"

	"wbolster_jsonlines/jsonlines"
)

var altSampleBytes = []byte(`{"m": 10}
{"n": 20}
`)
var altSampleText = string(altSampleBytes)

func isJSONDecodeErrorPublic(err error) bool {
	_, ok := err.(*json.SyntaxError)
	return ok
}

func TestPublicReader(t *testing.T) {
	reader := jsonlines.NewReader(bytes.NewReader(altSampleBytes))
	defer reader.Close()
	var obj map[string]interface{}
	if err := reader.Read(&obj); err != nil {
		t.Fatal(err)
	}
	if obj["m"] != float64(10) {
		t.Errorf("Expected {m:10}, got %v", obj)
	}
	if err := reader.Read(&obj); err != nil {
		t.Fatal(err)
	}
	if obj["n"] != float64(20) {
		t.Errorf("Expected {n:20}, got %v", obj)
	}
	var dummy map[string]interface{}
	err := reader.Read(&dummy)
	if err == nil || err == io.ErrUnexpectedEOF {
		t.Error("Expected EOF error")
	}
}

func TestPublicReadingFromIterable(t *testing.T) {
	input := []string{"5", `{"x":1}`}
	buf := bytes.NewBufferString("")
	for _, v := range input {
		buf.WriteString(v)
		buf.WriteString("\n")
	}
	reader := jsonlines.NewReader(buf)
	var out []interface{}
	for {
		var obj interface{}
		err := reader.Read(&obj)
		if err == io.EOF {
			break
		}
		out = append(out, obj)
	}
	expected := []interface{}{float64(5), map[string]interface{}{"x": float64(1)}}
	if !equalInterfaces(out, expected) {
		t.Errorf("Expected %v, got %v", expected, out)
	}
}

func TestPublicReaderRFC7464TextSequences(t *testing.T) {
	bs := []byte{0x1e, '"', 'A', '"', 0x0a, 0x1e, '"', 'B', '"', 0x0a}
	reader := jsonlines.NewReader(bytes.NewReader(bs))
	var vals []string
	for {
		var s string
		err := reader.Read(&s)
		if errors.Is(err, io.EOF) {
			break
		}
		vals = append(vals, s)
	}
	if len(vals) != 2 || vals[0] != "A" || vals[1] != "B" {
		t.Errorf("Expected ['A','B'], got %v", vals)
	}
}

func TestPublicReaderUtf8BOMBytes(t *testing.T) {
	// BOM, '3\n', BOM, '4\n'
	bom := []byte{0xef, 0xbb, 0xbf}
	chunks := append(append([]byte{}, bom...), []byte("3\n")...)
	chunks = append(chunks, bom...)
	chunks = append(chunks, []byte("4\n")...)
	reader := jsonlines.NewReader(bytes.NewReader(chunks))
	var vals []float64
	for {
		var f float64
		err := reader.Read(&f)
		if errors.Is(err, io.EOF) {
			break
		}
		vals = append(vals, f)
	}
	if len(vals) != 2 || vals[0] != 3 || vals[1] != 4 {
		t.Errorf("Vals: %v", vals)
	}
}

func TestPublicReaderUtf8BOMText(t *testing.T) {
	// "7\n" + BOM + "8\n"
	bom := string([]byte{0xef, 0xbb, 0xbf})
	chunks := []string{"7\n", bom, "8\n"}
	concat := chunks[0] + chunks[1] + chunks[2]
	reader := jsonlines.NewReader(bytes.NewBufferString(concat))
	var vals []float64
	for {
		var n float64
		err := reader.Read(&n)
		if errors.Is(err, io.EOF) {
			break
		}
		vals = append(vals, n)
	}
	if len(vals) != 2 || vals[0] != 7 || vals[1] != 8 {
		t.Errorf("UTF8 BOM lines: %v", vals)
	}
}

func TestPublicReaderUtf8BOMBOMBOM(t *testing.T) {
	bom := string([]byte{0xef, 0xbb, 0xbf})
	input := bom + bom + "17\n"
	reader := jsonlines.NewReader(bytes.NewBufferString(input))
	var n float64
	err := reader.Read(&n)
	if err == nil || !contains(err.Error(), "invalid json") {
		t.Errorf("Expected invalid json error, got %v", err)
	}
	if !isJSONDecodeErrorPublic(err) {
		t.Error("Expected json decode error")
	}
}

func TestPublicWriterText(t *testing.T) {
	var buf bytes.Buffer
	writer := jsonlines.NewWriter(&buf)
	writer.Write(map[string]interface{}{"alpha": 123})
	writer.Write(map[string]interface{}{"beta": 456})
	writer.Close()
	expected := `{"alpha":123}
{"beta":456}
`
	if buf.String() != expected {
		t.Errorf("Expected %q, got %q", expected, buf.String())
	}
}

func TestPublicWriterBinary(t *testing.T) {
	var buf bytes.Buffer
	writer := jsonlines.NewWriter(&buf)
	writer.Write(map[string]interface{}{"foo": 11})
	writer.Write(map[string]interface{}{"bar": 22})
	writer.Close()
	expected := `{"foo":11}
{"bar":22}
`
	if buf.String() != expected {
		t.Errorf("Expected %q, got %q", expected, buf.String())
	}
}

func TestPublicClosing(t *testing.T) {
	reader := jsonlines.NewReader(bytes.NewBuffer(nil))
	reader.Close()
	var out interface{}
	err := reader.Read(&out)
	if err == nil {
		t.Error("Expected error after close")
	}
	writer := jsonlines.NewWriter(io.Discard)
	writer.Close()
	writer.Close() // no-op
	if err := writer.Write(987); err == nil {
		t.Error("Expected error after writer closed")
	}
}

func TestPublicInvalidLines(t *testing.T) {
	data := "[9, 11"
	reader := jsonlines.NewReader(bytes.NewBufferString(data))
	var obj interface{}
	err := reader.Read(&obj)
	if err == nil || !contains(err.Error(), "invalid json") {
		t.Errorf("Expected invalid json error, got %v", err)
	}
	if err != nil && !contains(err.Error(), data) {
		t.Errorf("Expected err to contain input line")
	}
	if err != nil && !isJSONDecodeErrorPublic(err) {
		t.Errorf("Error is not json decode error")
	}
}

func TestPublicSkipInvalid(t *testing.T) {
	fp := bytes.NewBufferString("100\nbad\n200")
	reader := jsonlines.NewReader(fp)
	var vs []float64
	for i := 0; i < 3; i++ {
		var val float64
		err := reader.Read(&val)
		if err == nil {
			vs = append(vs, val)
		}
	}
	if vs[0] != 100 || vs[1] != 200 {
		t.Errorf("Expected 100,200, got %v", vs)
	}
}

func TestPublicEmptyStringsInIterable(t *testing.T) {
	input := []string{"789", "", "321"}
	buf := bytes.NewBufferString("")
	for _, v := range input {
		buf.WriteString(v)
		buf.WriteString("\n")
	}
	reader := jsonlines.NewReader(buf)
	var got []float64
	for i := 0; i < 3; i++ {
		var v float64
		err := reader.Read(&v)
		if err == nil {
			got = append(got, v)
		}
	}
	if got[0] != 789 || got[1] != 321 {
		t.Errorf("Expected 789,321 got %v", got)
	}
}

func TestPublicInvalidUtf8(t *testing.T) {
	// Produce bytes that are invalid UTF-8 (in Go they will decode to error on Unmarshal)
	reader := jsonlines.NewReader(bytes.NewReader([]byte{0xff, 0xff, '\n'}))
	var obj interface{}
	err := reader.Read(&obj)
	if err == nil {
		t.Error("Expected error for invalid utf-8")
	}
}

func TestPublicEmptyLines(t *testing.T) {
	buf := bytes.NewBuffer([]byte("55\n\n66\n"))
	reader := jsonlines.NewReader(buf)
	var val1 float64
	if err := reader.Read(&val1); err != nil {
		t.Fatalf("Read 1: %v", err)
	}
	var dummy interface{}
	err := reader.Read(&dummy)
	if err == nil {
		t.Errorf("Expected error for empty line")
	}
	var val2 float64
	if err := reader.Read(&val2); err != nil {
		t.Errorf("Read 2: %v", err)
	}
	err = reader.Read(&dummy)
	if err == nil {
		t.Errorf("Expected EOF at end")
	}
}

func TestPublicTypedReads(t *testing.T) {
	data := `43
false
"bar"
`
	reader := jsonlines.NewReader(bytes.NewBufferString(data))
	var n int
	if err := reader.Read(&n); err != nil {
		t.Errorf("Expected int, got %v", err)
	}
	var fail interface{}
	err := reader.Read(&fail)
	if err == nil {
		t.Errorf("Expected type error")
	}
	var failf interface{}
	err = reader.Read(&failf)
	if err == nil {
		t.Errorf("Expected type error")
	}
}

func TestPublicTypedReadInvalidType(t *testing.T) {
	reader := jsonlines.NewReader(bytes.NewBuffer(nil))
	var notvalid struct{ NotSomething string }
	err := reader.Read(&notvalid)
	if err == nil {
		t.Errorf("Expected type error for invalid struct type")
	}
}

func TestPublicTypedIteration(t *testing.T) {
	buf := bytes.NewBufferString("13\n14\n")
	reader := jsonlines.NewReader(buf)
	var val int
	var got []int
	for {
		if err := reader.Read(&val); err != nil {
			break
		}
		got = append(got, val)
	}
	if got[0] != 13 || got[1] != 14 {
		t.Errorf("Expected 13,14 got %v", got)
	}
}

// Supporting helpers
func contains(s, substr string) bool {
	return bytes.Contains([]byte(s), []byte(substr))
}

func equalInterfaces(a, b []interface{}) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		atypestr := typeOf(a[i])
		btypestr := typeOf(b[i])
		if atypestr != btypestr {
			return false
		}
		switch av := a[i].(type) {
		case float64, string, bool:
			if av != b[i] {
				return false
			}
		case map[string]interface{}:
			bv, ok := b[i].(map[string]interface{})
			if !ok {
				return false
			}
			aj, _ := json.Marshal(av)
			bj, _ := json.Marshal(bv)
			if !bytes.Equal(aj, bj) {
				return false
			}
		case []interface{}:
			bv, ok := b[i].([]interface{})
			if !ok {
				return false
			}
			if !equalInterfaces(av, bv) {
				return false
			}
		default:
			return false
		}
	}
	return true
}

func typeOf(x interface{}) string {
	switch x.(type) {
	case map[string]interface{}:
		return "map"
	case []interface{}:
		return "slice"
	case string:
		return "string"
	case float64:
		return "float"
	case bool:
		return "bool"
	default:
		return "unknown"
	}
}