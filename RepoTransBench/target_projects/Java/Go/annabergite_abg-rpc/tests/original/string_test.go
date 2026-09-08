package tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestGetBytesUtf8(t *testing.T) {
	str := "https://github.com/twitter/finagle/blob/master/finagle-netty4/src/main/scala/com/twitter/finagle/netty4/Netty4Listener.scala"
	got := []byte(str)
	assert.Equal(t, len(str), len(got))
}

func TestGetBytesAscii(t *testing.T) {
	str := "TestStr"
	got := []byte(str)
	assert.Equal(t, []byte(str), got)
}

func TestInstanceByNew(t *testing.T) {
	str := ""
	assert.Equal(t, "", str)
}