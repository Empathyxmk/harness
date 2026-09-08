package original

import (
	"testing"

	"yinjihuan_netty_im_go/tests"
)

func TestNoopImServerApp(t *testing.T) {
	_ = tests.NewImServerApp()
	// Just ensure this constructs successfully
}