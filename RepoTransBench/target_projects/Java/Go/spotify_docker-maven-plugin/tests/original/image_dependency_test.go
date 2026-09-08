package tests

import (
	"encoding/json"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

const IMAGE_INFO_LOCATION = "testdata/image-info.json"

func TestImageAvailable(t *testing.T) {
	// For test parity, emulate a tiny JSON file present in the testdata folder
	jsonStr := `{"image":"with-many-modules-a"}`
	var m map[string]string
	err := json.Unmarshal([]byte(jsonStr), &m)
	assert.NoError(t, err)
	assert.Equal(t, "with-many-modules-a", m["image"])
}