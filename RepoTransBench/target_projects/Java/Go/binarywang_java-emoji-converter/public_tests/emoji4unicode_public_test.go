package public_tests

import (
	"testing"
)

type Emoji4Unicode struct {
	categories interface{}
}
func (e *Emoji4Unicode) setCategories(v interface{}) {
	e.categories = v
}
func (e *Emoji4Unicode) getCategories() interface{} {
	return e.categories
}

func TestEmoji4UnicodePublicSettersAndGetters(t *testing.T) {
	unicode := &Emoji4Unicode{}
	unicode.setCategories(nil)
	if unicode.getCategories() != nil {
		t.Errorf("getCategories() != nil after setCategories(nil)")
	}
}