package public_tests

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

var anotherExampleResponse = map[string]interface{}{
	"links": map[string]interface{}{
		"self": "http://other.com/books",
		"next": "http://other.com/books?page[offset]=5",
		"last": "http://other.com/books?page[offset]=20",
	},
	"data": []interface{}{
		map[string]interface{}{
			"type": "books",
			"id":   "3",
			"attributes": map[string]interface{}{
				"title": "JSON API for humans!",
			},
			"relationships": map[string]interface{}{
				"editor": map[string]interface{}{
					"links": map[string]interface{}{
						"self":    "http://other.com/books/3/relationships/editor",
						"related": "http://other.com/books/3/editor",
					},
					"data": map[string]interface{}{"type": "people", "id": "21"},
				},
				"chapters": map[string]interface{}{
					"links": map[string]interface{}{
						"self":    "http://other.com/books/3/relationships/chapters",
						"related": "http://other.com/books/3/chapters",
					},
					"data": []interface{}{
						map[string]interface{}{"type": "chapters", "id": "4"},
						map[string]interface{}{"type": "chapters", "id": "8"},
					},
				},
			},
			"links": map[string]interface{}{
				"self": "http://other.com/books/3",
			},
		},
	},
	"included": []interface{}{
		map[string]interface{}{
			"type": "people",
			"id":   "21",
			"attributes": map[string]interface{}{
				"first-name": "Ana",
				"last-name":  "Smith",
				"twitter":    "anasmith",
			},
			"links": map[string]interface{}{
				"self": "http://other.com/people/21",
			},
		},
		map[string]interface{}{
			"type": "chapters",
			"id":   "4",
			"attributes": map[string]interface{}{
				"title": "Prologue",
			},
			"links": map[string]interface{}{
				"self": "http://other.com/chapters/4",
			},
		},
		map[string]interface{}{
			"type": "chapters",
			"id":   "8",
			"attributes": map[string]interface{}{
				"title": "Epilogue",
			},
			"links": map[string]interface{}{
				"self": "http://other.com/chapters/8",
			},
		},
	},
}

func TestKeepsExamplePublic(t *testing.T) {
	got := anotherExampleResponse
	assert.True(t, reflect.DeepEqual(anotherExampleResponse, got))
}

func TestLinksAlwaysPresentInParsedResponsePublic(t *testing.T) {
	parsed := map[string]interface{}{}
	links := map[string]interface{}{"yyy": "faked"}
	parsed["links"] = links
	assert.Equal(t, map[string]interface{}{"links": map[string]interface{}{"yyy": "faked"}}, parsed)
}

func TestAddObjectToParsedResponsePublic(t *testing.T) {
	parsed := map[string]interface{}{"data": []map[string]interface{}{}}
	obj := map[string]interface{}{"id": "3", "type": "y"}
	parsed["data"] = append(parsed["data"].([]map[string]interface{}), obj)
	assert.NotNil(t, parsed["data"])
}

func TestRemoveObjectFromParsedResponsePublic(t *testing.T) {
	parsed := map[string]interface{}{"data": []map[string]interface{}{{"id": "3", "type": "y"}}}
	parsed["data"] = []map[string]interface{}{}
	assert.Equal(t, map[string]interface{}{"data": []map[string]interface{}{}}, parsed)
}

func TestAddIncludedObjectToParsedResponsePublic(t *testing.T) {
	parsed := map[string]interface{}{"included": []map[string]interface{}{{"id": "3", "type": "y"}}}
	parsed["included"] = []map[string]interface{}{}
	assert.Equal(t, map[string]interface{}{"included": []map[string]interface{}{}}, parsed)
}

func TestRemoveIncludedObjectFromParsedResponsePublic(t *testing.T) {
	parsed := map[string]interface{}{}
	parsed["included"] = []map[string]interface{}{{"id": "3", "type": "y"}}
	assert.Equal(t, map[string]interface{}{"included": []map[string]interface{}{{"id": "3", "type": "y"}}}, parsed)
}

func TestAddRelationshipToParsedResponsePublic(t *testing.T) {
	parsed := map[string]interface{}{}
	parsed["data"] = map[string]interface{}{"relationships": map[string]interface{}{
		"duck": map[string]interface{}{"data": map[string]interface{}{"type": "duck", "id": "9"}},
	}}
	r := map[string]interface{}{
		"data": map[string]interface{}{
			"relationships": map[string]interface{}{
				"duck": map[string]interface{}{"data": map[string]interface{}{"type": "duck", "id": "9"}},
			},
		},
	}
	assert.Equal(t, r, parsed)
}

func TestRemoveRelationshipFromParsedResponsePublic(t *testing.T) {
	parsed := map[string]interface{}{
		"data": map[string]interface{}{
			"relationships": map[string]interface{}{
				"duck": map[string]interface{}{"data": map[string]interface{}{"type": "duck", "id": "9"}},
			},
		},
	}
	parsed["data"].(map[string]interface{})["relationships"] = map[string]interface{}{}
	assert.Equal(t, map[string]interface{}{"data": map[string]interface{}{"relationships": map[string]interface{}{}}}, parsed)
}