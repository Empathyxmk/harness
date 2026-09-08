package original

import (
	"errors"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

type WrongUser struct {
	Id       int
	Birthday interface{} // intentionally wrong (should be time.Time)
}

type CorrectUser struct {
	Id       int
	Birthday time.Time
}

func TestUndefinedDeserializer(t *testing.T) {
	dumped := map[string]interface{}{"id": 12, "birthday": "1879-03-14T11:30:00+01:00"}
	_, err := jsons.LoadWrongUser(dumped)
	assert.Error(t, err)
	assert.Equal(t, "No deserializer for type \"datetime\"", err.Error()) // mimic message
}

func TestWrongPrimitiveType(t *testing.T) {
	dumped := map[string]interface{}{"id": "Albert", "birthday": "1879-03-14T11:30:00+01:00"}
	_, err := jsons.LoadWrongUser(dumped)
	assert.Error(t, err)
	assert.Equal(t, "Could not cast \"Albert\" into \"int\"", err.Error()) // mimic message
}

func TestWrongType(t *testing.T) {
	dumped := map[string]interface{}{"id": 12, "birthday": "every day"}
	_, err := jsons.LoadCorrectUser(dumped)
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "Could not deserialize value")
	assert.Contains(t, err.Error(), "datetime.datetime")
}