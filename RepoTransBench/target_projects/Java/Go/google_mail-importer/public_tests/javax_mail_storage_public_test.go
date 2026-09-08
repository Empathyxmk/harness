package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Flags struct{ Draft bool }
type MimeMessage struct{ flags Flags }

func AddFlags(msg *MimeMessage, flags Flags) {
	if flags.Draft {
		msg.flags.Draft = true
	}
}

func TestCreateFlagDifferentInput(t *testing.T) {
	flags := Flags{}
	flags.Draft = true
	msg := &MimeMessage{}
	AddFlags(msg, flags)
	assert.True(t, msg.flags.Draft)
}