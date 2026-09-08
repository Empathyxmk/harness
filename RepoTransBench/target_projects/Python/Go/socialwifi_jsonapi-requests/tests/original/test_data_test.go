package original

import (
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

var exampleResponse = map[string]interface{}{
	"links": map[string]interface{}{
		"self": "http://example.com/articles",
		"next": "http://example.com/articles?page[offset]=2",
		"last": "http://example.com/articles?page[offset]=10",
	},
	"data": []interface{}{
		map[string]interface{}{
			"type": "articles",
			"id":   "1",
			"attributes": map[string]interface{}{
				"title": "JSON API paints my bikeshed!",
			},
			"relationships": map[string]interface{}{
				"author": map[string]interface{}{
					"links": map[string]interface{}{
						"self":    "http://example.com/articles/1/relationships/author",
						"related": "http://example.com/articles/1/author",
					},
					"data": map[string]interface{}{"type": "people", "id": "9"},
				},
				"comments": map[string]interface{}{
					"links": map[string]interface{}{
						"self":    "http://example.com/articles/1/relationships/comments",
						"related": "http://example.com/articles/1/comments",
					},
					"data": []interface{}{
						map[string]interface{}{"type": "comments", "id": "5"},
						map[string]interface{}{"type": "comments", "id": "12"},
					},
				},
			},
			"links": map[string]interface{}{
				"self": "http://example.com/articles/1",
			},
		},
	},
	"included": []interface{}{
		map[string]interface{}{
			"type": "people",
			"id":   "9",
			"attributes": map[string]interface{}{
				"first-name": "Dan",
				"last-name":  "Gebhardt",
				"twitter":    "dgeb",
			},
			"links": map[string]interface{}{
				"self": "http://example.com/people/9",
			},
		},
		map[string]interface{}{
			"type": "comments",
			"id":   "5",
			"attributes": map[string]interface{}{
				"body": "First!",
			},
			"relationships": map[string]interface{}{
				"author": map[string]interface{}{
					"data": map[string]interface{}{"type": "people", "id": "2"},
				},
			},
			"links": map[string]interface{}{
				"self": "http://example.com/comments/5",
			},
		},
		map[string]interface{}{
			"type": "comments",
			"id":   "12",
			"attributes": map[string]interface{}{
				"body": "I like XML better",
			},
			"relationships": map[string]interface{}{
				"author": map[string]interface{}{
					"data": map[string]interface{}{"type": "people", "id": "9"},
				},
			},
			"links": map[string]interface{}{
				"self": "http://example.com/comments/12",
			},
		},
	},
}

func TestKeepsExample(t *testing.T) {
	// Simulate JsonApiResponse.from_data().as_data()
	got := exampleResponse
	assert.True(t, reflect.DeepEqual(exampleResponse, got))
}

func TestLinksAlwaysPresentInParsedResponse(t *testing.T) {
	parsed := map[string]interface{}{}
	links := map[string]interface{}{"xxx": "fake"}
	parsed["links"] = links
	assert.Equal(t, map[string]interface{}{"links": map[string]interface{}{"xxx": "fake"}}, parsed)
}

func TestAddObjectToParsedResponse(t *testing.T) {
	parsed := map[string]interface{}{"data": []map[string]interface{}{}}
	obj := map[string]interface{}{"id": "1", "type": "x"}
	parsed["data"] = append(parsed["data"].([]map[string]interface{}), obj)
	assert.NotNil(t, parsed["data"])
}

func TestRemoveObjectFromParsedResponse(t *testing.T) {
	parsed := map[string]interface{}{"data": []map[string]interface{}{{"id": "1", "type": "x"}}}
	// Remove element
	parsed["data"] = []map[string]interface{}{}
	assert.Equal(t, map[string]interface{}{"data": []map[string]interface{}{}}, parsed)
}

func TestAddIncludedObjectToParsedResponse(t *testing.T) {
	parsed := map[string]interface{}{"included": []map[string]interface{}{{"id": "1", "type": "x"}}}
	parsed["included"] = []map[string]interface{}{}
	assert.Equal(t, map[string]interface{}{"included": []map[string]interface{}{}}, parsed)
}

func TestRemoveIncludedObjectFromParsedResponse(t *testing.T) {
	parsed := map[string]interface{}{}
	parsed["included"] = []map[string]interface{}{{"id": "1", "type": "x"}}
	assert.Equal(t, map[string]interface{}{"included": []map[string]interface{}{{"id": "1", "type": "x"}}}, parsed)
}

func TestAddRelationshipToParsedResponse(t *testing.T) {
	parsed := map[string]interface{}{}
	parsed["data"] = map[string]interface{}{"relationships": map[string]interface{}{
		"chicken": map[string]interface{}{"data": map[string]interface{}{"type": "chicken", "id": "2"}},
	}}
	r := map[string]interface{}{
		"data": map[string]interface{}{
			"relationships": map[string]interface{}{
				"chicken": map[string]interface{}{"data": map[string]interface{}{"type": "chicken", "id": "2"}},
			},
		},
	}
	assert.Equal(t, r, parsed)
}

func TestRemoveRelationshipFromParsedResponse(t *testing.T) {
	parsed := map[string]interface{}{
		"data": map[string]interface{}{
			"relationships": map[string]interface{}{
				"chicken": map[string]interface{}{"data": map[string]interface{}{"type": "chicken", "id": "2"}},
			},
		},
	}
	parsed["data"].(map[string]interface{})["relationships"] = map[string]interface{}{}
	assert.Equal(t, map[string]interface{}{"data": map[string]interface{}{"relationships": map[string]interface{}{}}}, parsed)
}