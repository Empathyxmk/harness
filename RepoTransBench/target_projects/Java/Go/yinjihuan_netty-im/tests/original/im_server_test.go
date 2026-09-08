package original

import (
	"testing"

	"yinjihuan_netty_im_go/tests"
)

func TestImServerInstantiation(t *testing.T) {
	_ = tests.NewImServer()
	// Just instantiate for coverage, no Netty logic
}