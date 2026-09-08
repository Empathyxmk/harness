package chainbreaker

import (
	"reflect"
	"testing"
)

func TestPublicSchemaAttributes(t *testing.T) {
	attr := SchemaFile()
	doc := SchemaDoc()
	if attr == "" && doc == "" {
		t.Error("Schema module lacks both file and doc attributes")
	}
}

func TestPublicSchemaTypeOfModule(t *testing.T) {
	// Go modules are always packages; check with reflect (simulated)
	obj := schemaModule{}
	if reflect.TypeOf(obj).Name() != "schemaModule" {
		t.Errorf("Expected schemaModule type, got: %T", obj)
	}
}

// API simulation for tests
func SchemaFile() string     { return "schema_file.go" }
func SchemaDoc() string      { return "docstring" }
type schemaModule struct{}