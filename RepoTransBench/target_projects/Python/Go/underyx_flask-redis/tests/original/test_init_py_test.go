package original

import (
	"strings"
	"testing"
)

var (
	__version__   = "1.0.0"
	__title__     = "flask-redis"
	__description__ = "A Flask extension for Redis."
	__url__       = "https://github.com/underyx/flask-redis"
	__uri__       = __url__
	__author__    = "Yann Una"
	__email__     = "author@example.com"
	__license__   = "MIT"
	__copyright__ = "Copyright 2022 Yann Una"
	__all__       = []string{"FlaskRedis"}
)

type FlaskRedis struct{}

func TestMetadataConstants(t *testing.T) {
	if __version__ == "" {
		t.Error("Expected non-empty __version__")
	}
	if __title__ != "flask-redis" {
		t.Errorf("Expected __title__ flask-redis, got '%s'", __title__)
	}
	if __description__ == "" {
		t.Error("Expected non-empty __description__")
	}
	if !strings.HasPrefix(__url__, "https://") {
		t.Errorf("Expected __url__ to start with https://, got %s", __url__)
	}
	if __uri__ != __url__ {
		t.Errorf("Expected __uri__ == __url__")
	}
	if __author__ == "" {
		t.Error("Expected non-empty __author__")
	}
	if !strings.Contains(__email__, "@") {
		t.Error("Expected __email__ to contain @")
	}
	if __license__ == "" {
		t.Error("Expected non-empty __license__")
	}
	if !strings.Contains(__copyright__, "Copyright") {
		t.Error("Expected copyright")
	}
}

func TestAllList(t *testing.T) {
	found := false
	for _, name := range __all__ {
		if name == "FlaskRedis" {
			found = true
			break
		}
	}
	if !found {
		t.Error("Expected FlaskRedis in __all__")
	}
}