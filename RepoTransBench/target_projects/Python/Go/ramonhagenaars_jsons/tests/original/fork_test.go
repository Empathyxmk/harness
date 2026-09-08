package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"ramonhagenaars_jsons/jsons"
)

func TestFork(t *testing.T) {
	f1 := jsons.Fork()
	f2 := jsons.Fork()
	f3 := jsons.ForkWithParent(f1)

	jsons.SetSerializer(f1, func(val string) interface{} { return "f1" })
	jsons.SetSerializer(f2, func(val string) interface{} { return "f2" })
	jsons.SetSerializer(f3, func(val int) interface{} { return 3 })

	f4 := jsons.ForkWithParent(f1)

	assert.Equal(t, "f1", jsons.DumpWithFork("fork!", f1))
	assert.Equal(t, "f2", jsons.DumpWithFork("fork!", f2))
	assert.Equal(t, "f3", jsons.DumpWithFork("f3", f3))
	assert.Equal(t, 3, jsons.DumpWithFork(42, f3))
	assert.Equal(t, "f1", jsons.DumpWithFork("fork!", f4))
}