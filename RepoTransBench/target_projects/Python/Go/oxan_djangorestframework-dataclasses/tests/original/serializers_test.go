package original

import (
	"testing"
)

type Data struct {
	Name  string `json:"name"`
	Count int    `json:"count"`
}

func SerializeData(d Data) map[string]interface{} {
	return map[string]interface{}{
		"name":  d.Name,
		"count": d.Count,
	}
}

func DeserializeData(m map[string]interface{}) Data {
	return Data{
		Name:  m["name"].(string),
		Count: m["count"].(int),
	}
}

func TestSerializeData(t *testing.T) {
	data := Data{"test", 42}
	result := SerializeData(data)
	if result["name"] != "test" || result["count"] != 42 {
		t.Errorf("Unexpected serialization: %+v", result)
	}
}

func TestDeserializeData(t *testing.T) {
	data := map[string]interface{}{
		"name":  "load",
		"count": 100,
	}
	result := DeserializeData(data)
	if result.Name != "load" || result.Count != 100 {
		t.Errorf("Unexpected deserialization: %+v", result)
	}
}