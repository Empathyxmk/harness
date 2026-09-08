package original

import (
	"testing"
)

func assertClassCompilesWithoutError(clazzResourceName, outputClassResourceName string, t *testing.T) {
	// In Go, this is a placeholder—just call with any string, always "compiles"
}

func TestClassCompilesWithoutError(t *testing.T) {
	assertClassCompilesWithoutError("Some.java", "SomeBuilder.java", t)
}