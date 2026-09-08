package original

import (
	"bytes"
	"encoding/gob"
	"errors"
	"io"
	"testing"
	"time"
)

// Person struct as in util/Person.java
type Person struct {
	ID   int
	Name string
}

// ---- deserialization interface -------
type TestDeserialize interface {
	Deserialize(io.Reader) error
}

// WithoutSerialKiller does regular gob decode
type TestDeserializeCommon struct{}

func (tdc *TestDeserializeCommon) Deserialize(r io.Reader) error {
	var p Person
	dec := gob.NewDecoder(r)
	if err := dec.Decode(&p); err != nil {
		return err
	}
	return nil
}

// WithSerialKiller would use a filtering stream (simulate)
type TestDeserializeSerialKiller struct{}

func (td *TestDeserializeSerialKiller) Deserialize(r io.Reader) error {
	// In real application, we'd simulate class filtering here.
	var p Person
	dec := gob.NewDecoder(r)
	if err := dec.Decode(&p); err != nil {
		return errors.New("blocked by SerialKiller-like filter: " + err.Error())
	}
	return nil
}

// ---- Test function ----

func TestSpeedTest(t *testing.T) {
	// Prepare object
	var buf bytes.Buffer
	personOut := Person{ID: 1, Name: "Test"}
	enc := gob.NewEncoder(&buf)
	if err := enc.Encode(personOut); err != nil {
		t.Fatalf("encode failed: %v", err)
	}

	speedTest(t, buf.Bytes(), &TestDeserializeCommon{}, false)
	speedTest(t, buf.Bytes(), &TestDeserializeSerialKiller{}, true)
}

func speedTest(t *testing.T, data []byte, d TestDeserialize, withSerialKiller bool) {
	// Warmup
	for i := 0; i < 1000; i++ {
		if err := d.Deserialize(bytes.NewReader(data)); err != nil {
			// ignore errors in warmup
		}
	}
	start := time.Now()
	for i := 0; i < 10000; i++ {
		if err := d.Deserialize(bytes.NewReader(data)); err != nil {
			// in real test, we'd handle failures; for demo, ignore
		}
	}
	elapsed := time.Since(start)
	if withSerialKiller {
		t.Logf("Result (WITH SerialKiller): %d ms for 10.000 iterations", elapsed.Milliseconds())
	} else {
		t.Logf("Result (WITHOUT SerialKiller): %d ms for 10.000 iterations", elapsed.Milliseconds())
	}
}