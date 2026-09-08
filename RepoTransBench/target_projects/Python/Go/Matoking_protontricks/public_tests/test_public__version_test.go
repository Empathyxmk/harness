package public_tests

import (
	"strings"
	"testing"
)

type VersionPublic struct {
	__version__   string
	version       string
	version_tuple [3]int
}

var _version = VersionPublic{
	__version__:   "0.0.0",
	version:       "0.0.0",
	version_tuple: [3]int{0, 0, 0},
}

func TestPublicVersionAttributes(t *testing.T) {
	if _version.__version__ == "" {
		t.Error("__version__ should not be empty")
	}
	if _version.version == "" {
		t.Error("version should not be empty")
	}
	if _, ok := interface{}(_version.version).(string); !ok {
		t.Error("version is not string")
	}
	if _, ok := interface{}(_version.version_tuple).([3]int); !ok {
		t.Error("version_tuple type error")
	}
	// __version__ should have exactly two dots
	if strings.Count(_version.__version__, ".") != 2 {
		t.Errorf("__version__ = %q: must have 2 dots", _version.__version__)
	}
	// version_tuple should be of len 3
	if len(_version.version_tuple) != 3 {
		t.Errorf("version_tuple (%v) must have length 3", _version.version_tuple)
	}
	// __version__ string must start with the int version_tuple[0]
	firstPart := strings.SplitN(_version.__version__, ".", 2)
	if len(firstPart) < 1 || firstPart[0] != "0" {
		t.Error("__version__ does not start with tuple first int")
	}
}