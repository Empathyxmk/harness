package public_tests

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
func (t *TestShardSupplier) GetShardForHost(host Host) string    { return host.hostname }

func TestShardSupplierPublic_Interface(t *testing.T) {
	shards := []string{"alpha", "beta"}
	supplier := NewTestShardSupplier(shards, "beta")
	gotShards := supplier.GetQueueShards()
	for _, k := range shards {
		if _, ok := gotShards[k]; !ok {
			t.Errorf("Shard %s not found", k)
		}
	}
	if supplier.GetCurrentShard() != "beta" {
		t.Errorf("Expected 'beta' as currentShard, got %s", supplier.GetCurrentShard())
	}
	host := Host{hostname: "hostY", port: 2, rack: "rackX", status: "Up"}
	if supplier.GetShardForHost(host) != "hostY" {
		t.Errorf("Expected host's hostname 'hostY', got %s", supplier.GetShardForHost(host))
	}
}

func TestShardSupplierPublic_EmptySet(t *testing.T) {
	supplier := NewTestShardSupplier([]string{}, "")
	if len(supplier.GetQueueShards()) != 0 {
		t.Errorf("Expected empty shards set")
	}
	if supplier.GetCurrentShard() != "" {
		t.Errorf("Expected nil current shard")
	}
}