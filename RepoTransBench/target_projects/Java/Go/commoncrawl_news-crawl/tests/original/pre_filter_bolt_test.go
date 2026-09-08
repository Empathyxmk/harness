package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Metadata struct {
	kv map[string][]string
}

func NewMetadata() *Metadata {
	return &Metadata{kv: map[string][]string{}}
}

func (m *Metadata) Set(key, value string) {
	m.kv[key] = append(m.kv[key], value)
}

func (m *Metadata) GetValues(key string) []string {
	return m.kv[key]
}

type Tuple struct {
	Fields map[string]interface{}
}

type OutputCollector struct {
	emitCalls      []interface{}
	emitStatus     []interface{}
	acknowledged   []*Tuple
	emittedStreams map[string][]interface{}
}

func NewOutputCollector() *OutputCollector {
	return &OutputCollector{emittedStreams: map[string][]interface{}{}}
}

type URLFilters struct {
	StubFilter func(url, metadata interface{}, value string) string
}

type PreFilterBolt struct {
	urlFilters *URLFilters
	collector  *OutputCollector
}

func NewPreFilterBolt() *PreFilterBolt {
	return &PreFilterBolt{
		urlFilters: &URLFilters{},
	}
}

func (b *PreFilterBolt) Prepare(collector *OutputCollector) {
	b.collector = collector
}

func (b *PreFilterBolt) Execute(tuple *Tuple) {
	url := tuple.Fields["url"].(string)
	metadata := tuple.Fields["metadata"].(*Metadata)
	filtered := b.urlFilters.StubFilter(nil, nil, url)
	if filtered == "" {
		metadata.Set("error.cause", "Filtered")
		b.collector.emittedStreams["status"] = append(b.collector.emittedStreams["status"], tuple)
	} else {
		b.collector.emitCalls = append(b.collector.emitCalls, tuple)
	}
	b.collector.acknowledged = append(b.collector.acknowledged, tuple)
}

func TestPreFilterBolt_UrlRejected(t *testing.T) {
	bolt := NewPreFilterBolt()
	bolt.urlFilters.StubFilter = func(url, metadata interface{}, value string) string {
		return ""
	}
	collector := NewOutputCollector()
	bolt.Prepare(collector)
	md := NewMetadata()
	tuple := &Tuple{Fields: map[string]interface{}{
		"url":      "http://reject.me",
		"metadata": md,
	}}
	bolt.Execute(tuple)

	// Checks
	assert.True(t, containsTuple(collector.emittedStreams["status"], tuple))
	assert.True(t, containsTuple(collector.acknowledged, tuple))
	assert.Equal(t, "Filtered", md.GetValues("error.cause")[0])
}

func TestPreFilterBolt_UrlAccepted(t *testing.T) {
	bolt := NewPreFilterBolt()
	bolt.urlFilters.StubFilter = func(url, metadata interface{}, value string) string {
		return "http://accept.me"
	}
	collector := NewOutputCollector()
	bolt.Prepare(collector)
	md := NewMetadata()
	tuple := &Tuple{Fields: map[string]interface{}{
		"url":      "http://accept.me",
		"metadata": md,
	}}
	bolt.Execute(tuple)

	assert.True(t, containsTuple(collector.emitCalls, tuple))
	assert.False(t, streamEmitContains(collector.emittedStreams["status"], tuple))
	assert.True(t, containsTuple(collector.acknowledged, tuple))
}

func containsTuple(list interface{}, target *Tuple) bool {
	switch vals := list.(type) {
	case []*Tuple:
		for _, t := range vals {
			if t == target {
				return true
			}
		}
	case []interface{}:
		for _, t := range vals {
			if tuple, ok := t.(*Tuple); ok && tuple == target {
				return true
			}
		}
	}
	return false
}

func streamEmitContains(lst interface{}, tup *Tuple) bool {
	return containsTuple(lst, tup)
}