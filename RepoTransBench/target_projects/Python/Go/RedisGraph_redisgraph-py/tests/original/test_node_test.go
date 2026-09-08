package original

import (
	"testing"

	"redisgraph/node"

	"github.com/stretchr/testify/assert"
)

func getTestNodes() (noArgs, noProps, propsOnly, noLabel, multiLabel *node.Node) {
	noArgs = node.NewNode()
	noProps = node.NewNodeWithIDAliasLabel(1, "alias", "l")
	propsOnly = node.NewNodeWithProperties(map[string]interface{}{"a": "a", "b": 10})
	noLabel = node.NewNodeWithIDAliasProperties(1, "alias", map[string]interface{}{"a": "a"})
	multiLabel = node.NewNodeWithIDAliasLabelList(1, "alias", []string{"l", "ll"})
	return
}

func TestNodeToString(t *testing.T) {
	noArgs, noProps, propsOnly, noLabel, multiLabel := getTestNodes()
	assert.Equal(t, "", noArgs.ToString())
	assert.Equal(t, "", noProps.ToString())
	assert.Equal(t, "", multiLabel.ToString())
	assert.Equal(t, `{a:"a",b:10}`, propsOnly.ToString())
	assert.Equal(t, `{a:"a"}`, noLabel.ToString())
}

func TestNodeStringify(t *testing.T) {
	noArgs, noProps, propsOnly, noLabel, multiLabel := getTestNodes()
	assert.Equal(t, "()", noArgs.String())
	assert.Equal(t, "(alias:l)", noProps.String())
	assert.Equal(t, "({a:\"a\",b:10})", propsOnly.String())
	assert.Equal(t, "(alias{a:\"a\"})", noLabel.String())
	assert.Equal(t, "(alias:l:ll)", multiLabel.String())
}

func TestNodeComparision(t *testing.T) {
	assert.Equal(t, node.NewNode(), node.NewNode())
	assert.Equal(t, node.NewNodeWithID(1), node.NewNodeWithID(1))
	assert.NotEqual(t, node.NewNodeWithID(1), node.NewNodeWithID(2))

	assert.Equal(t, node.NewNodeWithIDAlias(1, "a"), node.NewNodeWithIDAlias(1, "b"))
	assert.Equal(t, node.NewNodeWithIDAlias(1, "a"), node.NewNodeWithIDAlias(1, "a"))

	assert.Equal(t, node.NewNodeWithIDLabel(1, "a"), node.NewNodeWithIDLabel(1, "a"))
	assert.NotEqual(t, node.NewNodeWithIDLabel(1, "a"), node.NewNodeWithIDLabel(1, "b"))

	assert.Equal(t, node.NewNodeWithIDAliasLabel(1, "a", "l"), node.NewNodeWithIDAliasLabel(1, "a", "l"))
	assert.NotEqual(t, node.NewNodeWithAliasLabel("a", "l"), node.NewNodeWithAliasLabel("a", "l1"))

	assert.Equal(t, node.NewNodeWithAliasLabels("a", []string{"a", "b"}), node.NewNodeWithAliasLabels("a", []string{"a", "b"}))
	assert.NotEqual(t, node.NewNodeWithAliasLabels("a", []string{"a", "b"}), node.NewNodeWithAliasLabels("a", []string{"a", "c"}))

	assert.Equal(t, node.NewNodeWithProperties(map[string]interface{}{"a": 10}), node.NewNodeWithProperties(map[string]interface{}{"a": 10}))
	assert.NotEqual(t, node.NewNode(), node.NewNodeWithProperties(map[string]interface{}{"a": 10}))
}