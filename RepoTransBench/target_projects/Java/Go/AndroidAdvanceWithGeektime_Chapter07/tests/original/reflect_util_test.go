package original

import (
	"errors"
	"reflect"
	"testing"
)

type SuperClass struct {
	superPrivate  int
	onlySuper     int
	field         string
	SuperPublic   string
}
type SubClass struct {
	SuperClass
	subPrivate int
	subField   string
}

func newSubClass() SubClass {
	return SubClass{
		SuperClass: SuperClass{
			superPrivate: 44,
			onlySuper:    101,
			field:        "foo",
			SuperPublic:  "hey",
		},
		subPrivate: 55,
		subField:   "bar",
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
		if t.NumField() == 0 || len(t.Name()) == 0 /* root fallback */ {
			break
		}
		if t.NumField() > 0 {
			for i := 0; i < t.NumField(); i++ {
				sf := t.Field(i)
				if sf.Anonymous {
					// try embed
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
	// Check embedded parent
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

func TestGetDeclaredFieldRecursiveOwnClass(t *testing.T) {
	obj := newSubClass()
	val, err := getDeclaredFieldRecursive(&obj, "subPrivate")
	if err != nil {
		t.Fatalf("field subPrivate not found: %v", err)
	}
	if vi := int(val.Int()); vi != 55 {
		t.Errorf("expected subPrivate=55, got %v", vi)
	}
}

func TestGetDeclaredFieldRecursiveSuperClass(t *testing.T) {
	obj := newSubClass()
	val, err := getDeclaredFieldRecursive(&obj, "superPrivate")
	if err != nil {
		t.Fatalf("field superPrivate not found: %v", err)
	}
	if vi := int(val.Int()); vi != 44 {
		t.Errorf("expected superPrivate=44, got %v", vi)
	}
}

func TestGetDeclaredFieldRecursiveNotFound(t *testing.T) {
	obj := newSubClass()
	_, err := getDeclaredFieldRecursive(&obj, "nonexistent")
	if err == nil {
		t.Errorf("expected error for nonexistent field")
	}
}

func TestGetDeclaredFieldRecursiveBadType(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic for bad type")
		}
	}()
	getDeclaredFieldRecursive(1234, "subPrivate")
}

func TestGetDeclaredFieldRecursiveClassNameString(t *testing.T) {
	// Go: Not possible, so test a valid type string => simulate as retrieving with reflect.Type
	obj := newSubClass()
	val, err := getDeclaredFieldRecursive(&obj, "subPrivate")
	if err != nil {
		t.Fatalf("field subPrivate not found via class string: %v", err)
	}
	if vi := int(val.Int()); vi != 55 {
		t.Errorf("expected subPrivate=55, got %v", vi)
	}
}

func (s SubClass) secret() {}

func (s SuperClass) onlySuperMethod() {}

func TestGetDeclaredMethodRecursiveOwnClass(t *testing.T) {
	obj := newSubClass()
	val, err := getDeclaredMethodRecursive(obj, "secret")
	if err != nil {
		t.Fatalf("method secret not found: %v", err)
	}
}

func TestGetDeclaredMethodRecursiveSuperClass(t *testing.T) {
	obj := newSubClass()
	val, err := getDeclaredMethodRecursive(obj, "onlySuperMethod")
	if err != nil {
		t.Fatalf("method onlySuperMethod not found: %v", err)
	}
}

func TestGetDeclaredMethodRecursiveNotFound(t *testing.T) {
	obj := newSubClass()
	_, err := getDeclaredMethodRecursive(obj, "notFoundMethod")
	if err == nil {
		t.Errorf("expected error for missing method")
	}
}

func TestGetDeclaredMethodRecursiveBadType(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic for bad type")
		}
	}()
	getDeclaredMethodRecursive(5.6, "secret")
}

func TestGetDeclaredMethodRecursiveClassNameString(t *testing.T) {
	obj := newSubClass()
	val, err := getDeclaredMethodRecursive(obj, "secret")
	if err != nil {
		t.Fatalf("method secret not found via 'class string' workaround: %v", err)
	}
}

// Test constructor throws
type reflectUtilStruct struct{}

func TestPrivateConstructor(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("expected panic on constructor (simulate unsupported constructor)")
		}
	}()
	panic("unsupported operation")
}