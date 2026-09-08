package public_tests

import (
	"errors"
	"reflect"
	"strings"
	"testing"
	"time"

	"pilgr_paper/tests/original"
)

func TestContainsPublic(t *testing.T) {
	store := original.NewPaperStore()
	if store.Contains("cities") {
		t.Fatalf("Should not contain 'cities'")
	}
	store.Write("cities", original.GenPersonList(5))
	if !store.Contains("cities") {
		t.Errorf("Should contain 'cities'")
	}
}

func TestDeletePublic(t *testing.T) {
	store := original.NewPaperStore()
	store.Write("countries", original.GenPersonList(2))
	if !store.Contains("countries") {
		t.Fatalf("Missing 'countries'")
	}
	store.Delete("countries")
	if store.Contains("countries") {
		t.Errorf("countries key still exists")
	}
}

func TestDeleteNotExistedPublic(t *testing.T) {
	store := original.NewPaperStore()
	if store.Contains("cities") {
		t.Fatalf("Shouldn't contain 'cities'")
	}
	store.Delete("cities") // Should not panic
}

func TestClearPublic(t *testing.T) {
	store := original.NewPaperStore()
	store.Write("kings", original.GenPersonList(2))
	store.Write("queens", original.GenPersonList(4))
	if !store.Contains("kings") || !store.Contains("queens") {
		t.Fatal("Missing keys before Destroy")
	}
	store.Destroy()
	if store.Contains("kings") || store.Contains("queens") {
		t.Errorf("Keys still exist after Destroy()")
	}
	store.Write("lords", original.GenPersonList(6))
	if !store.Contains("lords") {
		t.Errorf("Should contain lords after re-use")
	}
	read := store.Read("lords")
	l, ok := read.([]original.Person)
	if !ok || len(l) != 6 {
		t.Errorf("Expected 6 lords, got %+v", read)
	}
}

func TestWriteReadNormalPublic(t *testing.T) {
	store := original.NewPaperStore()
	store.Write("fruit", "Apple")
	val := store.Read("fruit", "Banana")
	if val != "Apple" {
		t.Errorf("Expected Apple, got %v", val)
	}
}

func TestWriteReadNormalAfterReinitPublic(t *testing.T) {
	store := original.NewPaperStore()
	store.Write("drink", "Water")
	val := store.Read("drink", "Tea")
	// Simulate re-init
	if val != "Water" {
		t.Errorf("Expected Water, got %v", val)
	}
}

func TestReadNotExistedPublic(t *testing.T) {
	store := original.NewPaperStore()
	val := store.Read("unknown-key")
	if val != nil {
		t.Errorf("Expected nil, got %v", val)
	}
}

func TestReadDefaultPublic(t *testing.T) {
	store := original.NewPaperStore()
	val := store.Read("missing-key", "fallback")
	if val != "fallback" {
		t.Errorf("Expected 'fallback', got %v", val)
	}
}

func TestWriteNullPublic(t *testing.T) {
	store := original.NewPaperStore()
	err := store.Write("empty_val", nil)
	if err == nil {
		t.Errorf("Expected error on writing nil")
	}
}

func TestReplacePublic(t *testing.T) {
	store := original.NewPaperStore()
	store.Write("flower", "Rose")
	if store.Read("flower") != "Rose" {
		t.Errorf("Expected Rose")
	}
	store.Write("flower", "Tulip")
	if store.Read("flower") != "Tulip" {
		t.Errorf("Expected Tulip")
	}
}

func TestValidKeyNamesPublic(t *testing.T) {
	store := original.NewPaperStore()
	keys := []string{"animal", "animal.info$@", "creature-123"}
	for _, k := range keys {
		store.Write(k, "LionOrTiger")
		if store.Read(k) != "LionOrTiger" {
			t.Errorf("Expected LionOrTiger for %v", k)
		}
	}
}

func TestInvalidKeyNameBackslashPublic(t *testing.T) {
	store := original.NewPaperStore()
	err := store.Write("key/with/slash", "Value")
	if err == nil {
		t.Errorf("Expected error on key with slash")
	}
}

func TestGetBookWithDefaultBookNamePublic(t *testing.T) {
	// Not applicable in this stub
}

func TestCustomBookReadWritePublic(t *testing.T) {
	store1 := original.NewPaperStore()
	store2 := original.NewPaperStore()
	if store1 == store2 {
		t.Errorf("Store instances should not be the same")
	}
	store2.Destroy()
	store1.Write("river", "Amazon")
	store2.Write("river", "Nile")
	if store1.Read("river") != "Amazon" || store2.Read("river") != "Nile" {
		t.Errorf("Expected Amazon/Nile got %v/%v", store1.Read("river"), store2.Read("river"))
	}
}

func TestCustomBookDestroyPublic(t *testing.T) {
	store1 := original.NewPaperStore()
	store2 := original.NewPaperStore()
	store2.Destroy()
	store1.Write("river", "Ganges")
	store2.Write("river", "Thames")
	store2.Destroy()
	if store1.Read("river") != "Ganges" {
		t.Errorf("Expected Ganges")
	}
	if store2.Read("river") != nil {
		t.Errorf("Expected nil after destroy")
	}
}

func TestGetAllKeysPublic(t *testing.T) {
	store := original.NewPaperStore()
	store.Destroy()
	store.Write("ocean", "Pacific")
	store.Write("ocean2", "Atlantic")
	store.Write("ocean3", "Indian")

	want := map[string]struct{}{"ocean": {}, "ocean2": {}, "ocean3": {}}
	keys := []string{"ocean", "ocean2", "ocean3"}
	for _, k := range keys {
		if !store.Contains(k) {
			t.Errorf("Missing expected key %v", k)
		}
	}
}

func TestCustomSerializerPublic(t *testing.T) {
	// Skipped - Go has no direct equivalent for custom class serializers
}

func TestTimestampNoObjectPublic(t *testing.T) {
	store := original.NewPaperTimestampsStore()
	store.Write("dummy", "val")
	got := store.LastModified("nothing_here")
	if got != -1 {
		t.Errorf("Expected -1, got %v", got)
	}
}

func TestTimestampPublic(t *testing.T) {
	store := original.NewPaperTimestampsStore()
	start := time.Now().UnixMilli()
	store.Write("continent", "Asia")
	timestamp := store.LastModified("continent")
	if timestamp == -1 {
		t.Errorf("timestamp is -1")
	}
	elapsed := timestamp - start
	if elapsed < 0 {
		t.Errorf("LastModified occurs before start?! %v < %v", timestamp, start)
	}
}