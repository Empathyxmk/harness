package public_tests

import (
	"testing"
	"reflect"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestTupleDumpPublic(t *testing.T) {
	tuple := []interface{}{11, "world", 3.5}
	dumped := jsons.Dump(tuple)
	assert.True(t, reflect.DeepEqual([]interface{}{11, "world", 3.5}, dumped))
}

func TestTupleLoadPublic(t *testing.T) {
	data := []interface{}{42, "foo", 1.25}
	var loaded [3]interface{}
	err := jsons.Load(data, &loaded)
	assert.NoError(t, err)
	assert.Equal(t, [3]interface{}{42, "foo", 1.25}, loaded)
}