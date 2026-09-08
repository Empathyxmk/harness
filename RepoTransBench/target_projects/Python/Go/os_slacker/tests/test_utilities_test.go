package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// getItemIDByName is a translation of slacker.utilities.get_item_id_by_name.
// Minimal stub for demonstration; replace with actual function as needed.
func getItemIDByName(items []map[string]string, name string) string {
	for _, item := range items {
		if n, ok := item["name"]; ok && n == name {
			return item["id"]
		}
	}
	return ""
}

func TestGetItemIDByName(t *testing.T) {
	listDict := []map[string]string{
		{"name": "channel_name", "id": "123"},
		{},
	}
	id := getItemIDByName(listDict, "channel_name")
	assert.Equal(t, "123", id)
}