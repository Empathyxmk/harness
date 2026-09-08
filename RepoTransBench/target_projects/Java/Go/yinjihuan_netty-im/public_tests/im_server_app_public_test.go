package public_tests

import (
	"testing"

	"yinjihuan_netty_im_go/tests"
	"github.com/stretchr/testify/assert"
)

func TestCoverageViaNewInstance(t *testing.T) {
	app := tests.NewImServerApp()
	assert.Equal(t, "ImServerApp", app.ClassName())
}