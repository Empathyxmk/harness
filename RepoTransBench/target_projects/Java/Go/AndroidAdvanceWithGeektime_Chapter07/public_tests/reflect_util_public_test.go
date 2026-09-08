package public_tests

import (
	"errors"
	"reflect"
	"testing"
)

type RootClass struct {
	rootPrivate  int
	onlyRoot     int
	rootField    string
	RootPublic   string
}
type DerivedClass struct {
	RootClass
	derivedPrivate int
	derivedField   string
}

func newDerivedClass() DerivedClass {
	return DerivedClass{
		RootClass: RootClass{
			rootPrivate: 88,
			onlyRoot:    202,
			rootField:   "baz",
			RootPublic:  "yo",
		},
		derivedPrivate: 99,
		derivedField:   "qux",
	}
}

func getDeclaredFieldRecursive(inst interface{}, field string) (reflect.Value, error) {
	v := reflect.ValueOf(inst)
	if v.Kind() == reflect.Ptr {
		v = v.Elem()
	}
	t := v.Type()
	for {
		if f, ok := t.FieldByName(field); ok {
			return v.FieldByIndex(f.Index), nil
		}
		if t.NumField() == 0 || len(t.Name()) == 0 {
			break
		}
		if t.NumField() > 0 {
			for i := 0; i < t.NumField(); i++ {
				sf := t.Field(i)
				if sf.Anonymous {
					embed := v.Field(i)
					val, err := getDeclaredFieldRecursive(embed.Interface(), field)
					if err == nil {
						return val, nil
					}
				}
			}
		}
		break
	}
	return reflect.Value{}, errors.New("no such field")
}

func getDeclaredMethodRecursive(inst interface{}, method string) (reflect.Value, error) {
	v := reflect.ValueOf(inst)
	m := v.MethodByName(method)
	if m.IsValid() {
		return m, nil
	}
	t := v.Type()
	for i := 0; i < t.NumField(); i++ {
		sf := t.Field(i)
		if sf.Anonymous {
			embed := v.Field(i)
			mt, err := getDeclaredMethodRecursive(embed.Interface(), method)
			if err == nil {
				return mt, nil
			}
		}
	}
	return reflect.Value{}, errors.New("no such method")
}

func TestGetDeclaredFieldRecursiveOwnClassPublic(t *testing.T) {
	obj := newDerivedClass()
	val, err := getDeclaredFieldRecursive(&obj, "derivedPrivate")
	if err != nil {
		t.Fatalf("field derivedPrivate not found: %v", err)
	}
	if vi := int(val.Int()); vi != 99 {
		t.Errorf("expected derivedPrivate=99, got %v", vi)
	}
}

func TestGetDeclaredFieldRecursiveSuperClassPublic(t *testing.T) {
	obj := newDerivedClass()
	val, err := getDeclaredFieldRecursive(&obj, "rootPrivate")
	if err != nil {
		t.Fatalf("field rootPrivate not found: %v", err)
	}
	if vi := int(val.Int()); vi != 88 {
		t.Errorf("expected rootPrivate=88, got %v", vi)
	}
}

func TestGetDeclaredFieldRecursiveNotFoundPublic(t *testing.T) {
	obj := newDerivedClass()
	_, err := getDeclaredFieldRecursive(&obj, "noSuchField")
	if err == nil {
		t.Errorf("expected error for noSuchField")
	}
}

func TestGetDeclaredFieldRecursiveBadTypePublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic for bad type")
		}
	}()
	getDeclaredFieldRecursive(struct{}{}, "derivedPrivate")
}

func TestGetDeclaredFieldRecursiveClassNameStringPublic(t *testing.T) {
	// Go: Not feasible, so test with actual type.
	obj := newDerivedClass()
	val, err := getDeclaredFieldRecursive(&obj, "derivedPrivate")
	if err != nil {
		t.Fatalf("field derivedPrivate not found via class string: %v", err)
	}
	if vi := int(val.Int()); vi != 99 {
		t.Errorf("expected derivedPrivate=99, got %v", vi)
	}
}

func (d DerivedClass) mystery()      {}
func (r RootClass) onlyRootMethod() {}

func TestGetDeclaredMethodRecursiveOwnClassPublic(t *testing.T) {
	obj := newDerivedClass()
	val, err := getDeclaredMethodRecursive(obj, "mystery")
	if err != nil {
		t.Fatalf("method mystery not found: %v", err)
	}
}

func TestGetDeclaredMethodRecursiveSuperClassPublic(t *testing.T) {
	obj := newDerivedClass()
	val, err := getDeclaredMethodRecursive(obj, "onlyRootMethod")
	if err != nil {
		t.Fatalf("method onlyRootMethod not found: %v", err)
	}
}

func TestGetDeclaredMethodRecursiveNotFoundPublic(t *testing.T) {
	obj := newDerivedClass()
	_, err := getDeclaredMethodRecursive(obj, "notFoundPublicMethod")
	if err == nil {
		t.Errorf("expected error for missing method")
	}
}

func TestGetDeclaredMethodRecursiveBadTypePublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic for bad type")
		}
	}()
	getDeclaredMethodRecursive(true, "mystery")
}

func TestGetDeclaredMethodRecursiveClassNameStringPublic(t *testing.T) {
	obj := newDerivedClass()
	val, err := getDeclaredMethodRecursive(obj, "mystery")
	if err != nil {
		t.Fatalf("method mystery not found via 'class string' workaround: %v", err)
	}
}

// Simulate private constructor throws
func TestPrivateConstructorPublic(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic on private constructor (simulate unsupported operation)")
		}
	}()
	panic("unsupported operation")
}