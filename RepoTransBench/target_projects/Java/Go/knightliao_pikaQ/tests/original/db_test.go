package original

import "testing"

const DB_NAME = "pikaqDemoWeb"

func TestDBNameConstant(t *testing.T) {
	if DB_NAME != "pikaqDemoWeb" {
		t.Errorf("DB.NAME = %s, expected pikaqDemoWeb", DB_NAME)
	}
}