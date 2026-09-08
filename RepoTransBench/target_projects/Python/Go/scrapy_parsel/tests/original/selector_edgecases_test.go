package original

import (
	"testing"
	"errors"
	"github.com/stretchr/testify/assert"
	parsel "scrapy_parsel/parsel"
)

func TestSelectorListGetStateNotPickle(t *testing.T) {
	list := parsel.NewSelectorList()
	_, err := list.GetState()
	assert.Error(t, err)
	assert.True(t, errors.Is(err, parsel.ErrNotPickle))
}

func TestRootNodeEmptyTextHTML(t *testing.T) {
	node := parsel.CreateRootNode("", "html")
	assert.NotNil(t, node)
}

func TestRootNodeHugeTreeWarn(t *testing.T) {
	// Simulate LXML_SUPPORTS_HUGE_TREE being false and warning emitted
	parsel.SetLxmlSupportsHugeTree(false)
	warnings := []string{}
	parsel.SetWarningFunc(func(msg string) {
		warnings = append(warnings, msg)
	})
	node := parsel.CreateRootNode("test", "html")
	assert.NotNil(t, node)
	assert.True(t, len(warnings) > 0)
}

func TestExceptionsInheritance(t *testing.T) {
	assert.True(t, parsel.IsSubclass(parsel.ErrCannotDropElementWithoutParent, parsel.ErrCannotRemoveElementWithoutParent))
	assert.True(t, parsel.IsSubclass(parsel.ErrCannotRemoveElementWithoutParent, parsel.ErrBaseException))
	assert.True(t, parsel.IsSubclass(parsel.ErrCannotRemoveElementWithoutRoot, parsel.ErrBaseException))
}