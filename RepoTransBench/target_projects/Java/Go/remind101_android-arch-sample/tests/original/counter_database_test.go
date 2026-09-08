package original

import (
	"testing"
)

func TestCounterDatabase_GetInstanceSingleton(t *testing.T) {
	db1 := GetCounterDatabase()
	db2 := GetCounterDatabase()
	if db1 != db2 {
		t.Errorf("CounterDatabase is not a singleton")
	}
}

func TestCounterDatabase_SaveAndGetCounter(t *testing.T) {
	db := GetCounterDatabase()
	db.Clear()
	counter := newCounter()
	counter.SetValue(15)
	db.SaveCounter(counter)

	result := db.GetCounter(counter.GetId())
	if result == nil {
		t.Fatalf("Expected to find saved counter")
	}
	if result.GetId() != counter.GetId() {
		t.Errorf("GetCounter returned wrong id. Got %d, want %d", result.GetId(), counter.GetId())
	}
	if result.GetValue() != 15 {
		t.Errorf("Counter value mismatch: got %d, want 15", result.GetValue())
	}
}

func TestCounterDatabase_GetCounterNotFound(t *testing.T) {
	db := GetCounterDatabase()
	db.Clear()
	result := db.GetCounter(-1)
	if result != nil {
		t.Errorf("Expected nil for unknown counter id")
	}
}

func TestCounterDatabase_GetAllCounters(t *testing.T) {
	db := GetCounterDatabase()
	db.Clear()
	counter1 := newCounter()
	counter1.SetValue(5)
	db.SaveCounter(counter1)

	counter2 := newCounter()
	counter2.SetValue(11)
	db.SaveCounter(counter2)

	list := db.GetAllCounters()
	if len(list) < 2 {
		t.Errorf("CounterDatabase list should have at least 2: got %d", len(list))
	}
	for _, c := range list {
		if c.GetId() == 0 {
			t.Errorf("Counter ID should be non-zero")
		}
	}
}