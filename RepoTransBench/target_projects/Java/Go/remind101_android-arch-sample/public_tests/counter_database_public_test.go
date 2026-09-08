package public_tests

import "testing"

func TestCounterDatabasePublicTest_GetInstanceReturnsSameDatabase(t *testing.T) {
	db := GetCounterDatabase()
	db2 := GetCounterDatabase()
	if db != db2 {
		t.Errorf("Databases not same instance")
	}
}

func TestCounterDatabasePublicTest_SaveAndGetCounterWithDifferentValue(t *testing.T) {
	db := GetCounterDatabase()
	db.Clear()
	counter := newCounter()
	counter.SetValue(37)
	db.SaveCounter(counter)
	result := db.GetCounter(counter.GetId())
	if result == nil {
		t.Fatalf("Saved counter not found")
	}
	if result.GetId() != counter.GetId() {
		t.Errorf("Counter IDs do not match: %d vs %d", result.GetId(), counter.GetId())
	}
	if result.GetValue() != 37 {
		t.Errorf("Counter value mismatch: got %d, want 37", result.GetValue())
	}
}

func TestCounterDatabasePublicTest_GetCounterWithAbsentId(t *testing.T) {
	db := GetCounterDatabase()
	db.Clear()
	result := db.GetCounter(-42)
	if result != nil {
		t.Errorf("Expected nil for unknown counter id")
	}
}

func TestCounterDatabasePublicTest_GetAllCountersShouldContainMultipleWithDifferentValues(t *testing.T) {
	db := GetCounterDatabase()
	db.Clear()
	counter1 := newCounter()
	counter1.SetValue(23)
	db.SaveCounter(counter1)
	counter2 := newCounter()
	counter2.SetValue(99)
	db.SaveCounter(counter2)
	list := db.GetAllCounters()
	if len(list) < 2 {
		t.Errorf("Should have at least 2 counters")
	}
	for _, c := range list {
		if c.GetId() <= 0 {
			t.Errorf("Counter ID should be > 0, got %d", c.GetId())
		}
	}
}