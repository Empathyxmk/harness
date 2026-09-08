package original

import (
	"testing"

	"redisgraph/node"
	"redisgraph/edge"

	"github.com/stretchr/testify/assert"
)

func TestEdgeInit(t *testing.T) {
	assert.Panics(t, func() {
		edge.NewEdge(nil, nil, nil)
	})

	assert.Panics(t, func() {
		edge.NewEdge(node.NewNode(), nil, nil)
	})

	assert.Panics(t, func() {
		edge.NewEdge(nil, nil, node.NewNode())
	})

	e := edge.NewEdge(node.NewNodeWithID(1), nil, node.NewNodeWithID(2))
	assert.NotNil(t, e)
}

func TestEdgeToString(t *testing.T) {
	propsResult := edge.NewEdge(node.NewNode(), nil, node.NewNode(), edge.WithProperties(map[string]interface{}{"a": "a", "b": 10})).ToString()
	assert.Equal(t, `{a:"a",b:10}`, propsResult)

	noPropsResult := edge.NewEdge(node.NewNode(), nil, node.NewNode(), edge.WithProperties(map[string]interface{}{})).ToString()
	assert.Equal(t, ``, noPropsResult)
}

func TestEdgeStringify(t *testing.T) {
	john := node.NewNodeWithAliasLabelProps("a", "person", map[string]interface{}{"name": "John Doe", "age": 33, "someArray": []interface{}{1, 2, 3}})
	japan := node.NewNodeWithAliasLabelProps("b", "country", map[string]interface{}{"name": "Japan"})
	edgeWithRelation := edge.NewEdge(john, "visited", japan, edge.WithProperties(map[string]interface{}{"purpose": "pleasure"}))

	assert.Equal(t,
		`(a:person{age:33,name:"John Doe",someArray:[1, 2, 3]})-[:visited{purpose:"pleasure"}]->(b:country{name:"Japan"})`,
		edgeWithRelation.String(),
	)

	edgeNoRelationNoProps := edge.NewEdge(japan, "", john)
	assert.Equal(t,
		`(b:country{name:"Japan"})-[]->(a:person{age:33,name:"John Doe",someArray:[1, 2, 3]})`,
		edgeNoRelationNoProps.String(),
	)

	edgeOnlyProps := edge.NewEdge(john, "", japan, edge.WithProperties(map[string]interface{}{"a": "b", "c": 3}))
	assert.Equal(t,
		`(a:person{age:33,name:"John Doe",someArray:[1, 2, 3]})-[{a:"b",c:3}]->(b:country{name:"Japan"})`,
		edgeOnlyProps.String(),
	)
}

func TestEdgeComparision(t *testing.T) {
	node1 := node.NewNodeWithID(1)
	node2 := node.NewNodeWithID(2)
	node3 := node.NewNodeWithID(3)

	edge1 := edge.NewEdge(node1, nil, node2)
	assert.Equal(t, edge1, edge.NewEdge(node1, nil, node2))
	assert.NotEqual(t, edge1, edge.NewEdge(node1, "bla", node2))
	assert.NotEqual(t, edge1, edge.NewEdge(node1, nil, node3))
	assert.NotEqual(t, edge1, edge.NewEdge(node3, nil, node2))
	assert.NotEqual(t, edge1, edge.NewEdge(node2, nil, node1))
	assert.NotEqual(t, edge1, edge.NewEdge(node1, nil, node2, edge.WithProperties(map[string]interface{}{"a": 10})))
}