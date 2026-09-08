package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// getItemIDByNamePublic is a translation of slacker.utilities.get_item_id_by_name
func getItemIDByNamePublic(items []map[string]string, name string) string {
	for _, item := range items {
		if n, ok := item["name"]; ok && n == name {
			return item["id"]
		}
	}
	return ""
}

func TestGetItemIDByNamePublic(t *testing.T) {
	listDict := []map[string]string{
		{"name": "public_channel", "id": "789"},
		{"name": "other", "id": "456"},
	}
	id := getItemIDByNamePublic(listDict, "public_channel")
	assert.Equal(t, "789", id)
}