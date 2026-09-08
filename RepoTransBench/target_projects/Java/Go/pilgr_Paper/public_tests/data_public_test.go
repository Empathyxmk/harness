package public_tests

import (
	"reflect"
	"sync"
	"testing"
	"time"

	"pilgr_paper/tests/original"
)

func TestPutEmptyListPublic(t *testing.T) {
	store := original.NewPaperStore()
	inserted := original.GenPersonList(3)
	if err := store.Write("persons_pub", inserted); err != nil {
		t.Fatalf("Write failed: %v", err)
	}
	read := store.Read("persons_pub")
	persons, ok := read.([]original.Person)
	if !ok || len(persons) != 3 {
		t.Errorf("Expected 3 persons, got %+v", read)
	}
	// Overwrite with empty
	if err := store.Write("persons_pub", []original.Person{}); err != nil {
		t.Fatalf("Write failed: %v", err)
	}
	read2 := store.Read("persons_pub")
	persons2, ok := read2.([]original.Person)
	if !ok || len(persons2) != 0 {
		t.Errorf("Expected 0 persons, got %+v", read2)
	}
}

func TestPutGetListPublic(t *testing.T) {
	store := original.NewPaperStore()
	inserted := original.GenPersonList(7)
	if err := store.Write("alt_persons", inserted); err != nil {
		t.Fatalf("Write failed: %v", err)
	}
	read := store.Read("alt_persons")
	if !original.DeepEqual(read, inserted) {
		t.Errorf("Persons mismatch. Got %+v, want %+v", read, inserted)
	}
}

func TestPutMapPublic(t *testing.T) {
	store := original.NewPaperStore()
	inserted := original.GenPersonMap(5)
	if err := store.Write("alt_persons_map", inserted); err != nil {
		t.Fatalf("Write failed: %v", err)
	}
	read := store.Read("alt_persons_map")
	if !original.DeepEqual(read, inserted) {
		t.Errorf("Map mismatch. Got %+v, want %+v", read, inserted)
	}
}

func TestPutPOJOPublic(t *testing.T) {
	store := original.NewPaperStore()
	person := original.GenPerson(original.Person{}, 42)
	if err := store.Write("new_profile", person); err != nil {
		t.Fatalf("Write failed: %v", err)
	}
	read := store.Read("new_profile")
	if !original.DeepEqual(read, person) {
		t.Errorf("Person mismatch.")
	}
	if &read == &person {
		t.Errorf("Expected different object pointers after read/write.")
	}
}

func TestPutSubAbstractListRandomAccessPublic(t *testing.T) {
	store := original.NewPaperStore()
	origin := original.GenPersonList(20)
	sublist := origin[5:17]
	testReadWriteWithoutClassCheckPublic(t, store, sublist)
}

func TestPutSubAbstractListPublic(t *testing.T) {
	store := original.NewPaperStore()
	origin := original.GenPersonList(20)
	sublist := origin[5:17]
	testReadWriteWithoutClassCheckPublic(t, store, sublist)
}

func TestPutLinkedListPublic(t *testing.T) {
	store := original.NewPaperStore()
	origin := original.GenPersonList(15)
	testReadWritePublic(t, store, origin)
}

func TestPutArraysAsListsPublic(t *testing.T) {
	store := original.NewPaperStore()
	arr := []string{"abc", "xyz", "def"}
	testReadWritePublic(t, store, arr)
}

func TestPutCollectionsEmptyListPublic(t *testing.T) {
	store := original.NewPaperStore()
	arr := []string{}
	testReadWritePublic(t, store, arr)
}

func TestPutCollectionsEmptyMapPublic(t *testing.T) {
	store := original.NewPaperStore()
	m := map[int]string{}
	testReadWritePublic(t, store, m)
}

func TestPutCollectionsEmptySetPublic(t *testing.T) {
	store := original.NewPaperStore()
	set := make(map[string]struct{})
	testReadWritePublic(t, store, set)
}

func TestPutSingletonListPublic(t *testing.T) {
	store := original.NewPaperStore()
	arr := []string{"singleton_item"}
	testReadWritePublic(t, store, arr)
}

func TestPutSingletonSetPublic(t *testing.T) {
	store := original.NewPaperStore()
	set := map[string]struct{}{"singleton": {}}
	testReadWritePublic(t, store, set)
}

func TestPutSingletonMapPublic(t *testing.T) {
	store := original.NewPaperStore()
	m := map[string]string{"onlykey": "onlyvalue"}
	testReadWritePublic(t, store, m)
}

func TestPutGeorgianCalendarPublic(t *testing.T) {
	store := original.NewPaperStore()
	now := time.Date(1999, 9, 13, 0, 0, 0, 0, time.UTC) // Sept=9, like Java Calendar.MONTH==8, Java uses 0-based index
	testReadWritePublic(t, store, now)
}

// Simulating a synchronized list just uses a slice with mutex in Go, though not needed for test
func TestPutSynchronizedListPublic(t *testing.T) {
	store := original.NewPaperStore()
	arr := []string{"hello"}
	var mu sync.Mutex
	mu.Lock()
	testReadWritePublic(t, store, arr)
	mu.Unlock()
}

func TestReadWriteClassWithoutNoArgConstructorPublic(t *testing.T) {
	store := original.NewPaperStore()
	obj := original.PersonArg{Name: "alice"}
	testReadWritePublic(t, store, obj)
}

// Helpers for this suite
func testReadWriteWithoutClassCheckPublic(t *testing.T, store *original.PaperStore, originObj interface{}) interface{} {
	if err := store.Write("obj_pub", originObj); err != nil {
		t.Fatal(err)
	}
	readObj := store.Read("obj_pub")
	if !reflect.DeepEqual(readObj, originObj) {
		t.Fatalf("Objects not equal after read/write. Got %+v, want %+v", readObj, originObj)
	}
	return readObj
}

func testReadWritePublic(t *testing.T, store *original.PaperStore, originObj interface{}) {
	readObj := testReadWriteWithoutClassCheckPublic(t, store, originObj)
	if reflect.TypeOf(readObj) != reflect.TypeOf(originObj) {
		t.Errorf("Expected same class after read/write. Got %T, want %T", readObj, originObj)
	}
}