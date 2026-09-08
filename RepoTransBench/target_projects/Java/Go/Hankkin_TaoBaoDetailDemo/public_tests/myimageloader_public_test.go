package public_tests

import (
	"testing"
)

type MyImageLoader struct{}

var myImageLoaderPublicInstance *MyImageLoader

func GetMyImageLoaderPublicInstance() *MyImageLoader {
	if myImageLoaderPublicInstance == nil {
		myImageLoaderPublicInstance = &MyImageLoader{}
	}
	return myImageLoaderPublicInstance
}

// Test equivalent for: MyImageLoaderPublicTest.java
func TestMyImageLoader_PublicSingletonInstanceDifferentCallNotNull(t *testing.T) {
	instanceA := GetMyImageLoaderPublicInstance()
	instanceB := GetMyImageLoaderPublicInstance()
	if instanceA == nil {
		t.Error("First singleton instance got nil")
	}
	if instanceB == nil {
		t.Error("Second singleton instance got nil")
	}
	if instanceA != instanceB {
		t.Error("Expected singleton instances to be the same (got different pointers)")
	}
}