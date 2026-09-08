package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
	"precommit_hooks"
)

func TestAlwaysFails(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			err, ok := r.(error)
			assert.True(t, ok)
			if ok {
				assert.Equal(t, "`autopep8-wrapper` has been removed -- use `autopep8` from https://github.com/pre-commit/mirrors-autopep8", err.Error())
			}
		} else {
			t.Fail()
		}
	}()
	precommit_hooks.RemovedMain([]string{
		"autopep8-wrapper", "autopep8",
		"https://github.com/pre-commit/mirrors-autopep8",
		"--foo", "bar",
	})
}