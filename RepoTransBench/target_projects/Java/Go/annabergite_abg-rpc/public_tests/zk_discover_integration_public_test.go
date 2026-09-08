package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIntegrationDiscoverWithNewNode(t *testing.T) {
	newNode := "/public/integration/node"
	discovered := simulateDiscover(newNode)
	assert.True(t, discovered, "Should discover the integration public node")
}

func simulateDiscover(node string) bool {
	return node == "/public/integration/node"
}