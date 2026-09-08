package original

import (
	"testing"

	"bytes"
	"encoding/hex"

	"github.com/stretchr/testify/assert"
	"github.com/socialwifi_routeros_api/routeros_api/api_socket"
)

func TestEncodeToApi(t *testing.T) {
	cases := []struct {
		raw    []string
		expect string
	}{
		{[]string{"!login"}, "000600216c6f67696e"},
		{[]string{"=name=admin", "=password=test"}, "000c3d6e616d653d61646d696e000f3d70617373776f72643d74657374"},
		{[]string{"=name=bączek"}, "000d3d6e616d653db485637a656b"},
	}

	for _, tc := range cases {
		pkt := api_socket.EncodeToApi(tc.raw)
		assert.Equal(t, tc.expect, hex.EncodeToString(pkt))
	}
}

func TestReadLength(t *testing.T) {
	cases := []struct {
		data     []byte
		expected int
		offset   int
	}{
		{[]byte{10}, 10, 1},
		{[]byte{0x81, 0x01}, 129, 2},
		{[]byte{0xC0, 0x00, 0x01}, 16385, 3},
		{[]byte{0xFF, 0xFF, 0xFF, 0x7F}, 0x7FFFFFFF, 4},
	}

	for _, tc := range cases {
		val, off := api_socket.ReadLength(tc.data)
		assert.Equal(t, tc.expected, val)
		assert.Equal(t, tc.offset, off)
	}
}

func TestDecodeFromApi(t *testing.T) {
	// The packet corresponds to two words: !done, =ret=abc
	b, _ := hex.DecodeString("00060021646f6e6500093d7265743d616263")
	words, err := api_socket.DecodeFromApi(b)
	assert.NoError(t, err)
	assert.Equal(t, []string{"!done", "=ret=abc"}, words)
}

func TestBuildSentence(t *testing.T) {
	words := []string{"foo", "bar", "baz"}
	encoded := api_socket.EncodeToApi(words)
	decoded, err := api_socket.DecodeFromApi(encoded)
	assert.NoError(t, err)
	assert.Equal(t, words, decoded)
}

func TestEncodeDecodeEmpty(t *testing.T) {
	words := []string{}
	encoded := api_socket.EncodeToApi(words)
	assert.Equal(t, []byte{}, encoded)
	decoded, err := api_socket.DecodeFromApi(encoded)
	assert.NoError(t, err)
	assert.Equal(t, []string{}, decoded)
}

func TestDecodeLengthError(t *testing.T) {
	invalid := []byte{0x82}
	_, err := api_socket.DecodeFromApi(invalid)
	assert.Error(t, err)
}

func TestEncodeUnicodeWord(t *testing.T) {
	words := []string{"ą"} // c4 85
	encoded := api_socket.EncodeToApi(words)
	decoded, err := api_socket.DecodeFromApi(encoded)
	assert.NoError(t, err)
	assert.Equal(t, words, decoded)
}

func TestEncodeToApiMultiple(t *testing.T) {
	words := []string{"test", "abc", "123"}
	encoded := api_socket.EncodeToApi(words)
	decoded, err := api_socket.DecodeFromApi(encoded)
	assert.NoError(t, err)
	assert.Equal(t, words, decoded)
}

func TestRoundtripRandomBinary(t *testing.T) {
	raw := []string{"błąd", string([]byte{0, 1, 2, 255})}
	encoded := api_socket.EncodeToApi(raw)
	decoded, err := api_socket.DecodeFromApi(encoded)
	assert.NoError(t, err)
	assert.Equal(t, raw, decoded)
}

func TestWriteLength(t *testing.T) {
	cases := []struct {
		length int
		expect []byte
	}{
		{0, []byte{0}},
		{5, []byte{5}},
		{129, []byte{0x81, 0x01}},
		{16385, []byte{0xC0, 0x00, 0x01}},
		{0x7FFFFFFF, []byte{0xFF, 0xFF, 0xFF, 0x7F}},
	}

	for _, tc := range cases {
		got := api_socket.WriteLength(tc.length)
		assert.True(t, bytes.Equal(got, tc.expect))
	}
}

func TestBadDecodeTrailingData(t *testing.T) {
	hexstr := "000400666f6f00" // extra byte at end
	pkt, _ := hex.DecodeString(hexstr)
	_, err := api_socket.DecodeFromApi(pkt)
	assert.Error(t, err)
}