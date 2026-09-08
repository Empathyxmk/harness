package original

import (
	"testing"
)

type Host struct {
	hostname string
	port     int
	rack     string
	status   string
}

type ShardSupplier interface {
	GetQueueShards() map[string]struct{}
	GetCurrentShard() string
	GetShardForHost(host Host) string
}

type TestShardSupplier struct {
	shards       map[string]struct{}
	currentShard string
}

func NewTestShardSupplier(shards []string, currentShard string) *TestShardSupplier {
	set := make(map[string]struct{})
	for _, s := range shards {
		set[s] = struct{}{}
	}
	return &TestShardSupplier{shards: set, currentShard: currentShard}
}

func (t *TestShardSupplier) GetQueueShards() map[string]struct{} { return t.shards }
func (t *TestShardSupplier) GetCurrentShard() string             { return t.currentShard }
func (t *TestShardSupplier) GetShardForHost(host Host) string    { return host.rack }

func TestShardSupplierInterface(t *testing.T) {
	shards := []string{"one", "two"}
	supplier := NewTestShardSupplier(shards, "one")
	gotShards := supplier.GetQueueShards()
	for _, k := range shards {
		if _, ok := gotShards[k]; !ok {
			t.Errorf("Shard %s not found", k)
		}
	}
	if supplier.GetCurrentShard() != "one" {
		t.Errorf("Expected 'one' as currentShard, got %s", supplier.GetCurrentShard())
	}
	host := Host{hostname: "host", port: 1, rack: "rck", status: "Up"}
	if supplier.GetShardForHost(host) != "rck" {
		t.Errorf("Expected rack to be 'rck', got %s", supplier.GetShardForHost(host))
	}
}

func TestShardSupplierEmptySet(t *testing.T) {
	supplier := NewTestShardSupplier([]string{}, "")
	if len(supplier.GetQueueShards()) != 0 {
		t.Errorf("Expected empty shards set")
	}
	if supplier.GetCurrentShard() != "" {
		t.Errorf("Expected nil current shard")
	}
}