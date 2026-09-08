package public_tests

import (
	"net/url"
	"testing"

	"github.com/stretchr/testify/assert"
)

type GatewayOptions struct {
	PrintHelp     bool
	Port          *int
	DefaultConfig *url.URL
	Jars          []url.URL
	LibraryDirs   []url.URL
}

func (opts GatewayOptions) IsPrintHelp() bool         { return opts.PrintHelp }
func (opts GatewayOptions) GetPort() *int             { return opts.Port }
func (opts GatewayOptions) GetDefaultConfig() *url.URL { return opts.DefaultConfig }
func (opts GatewayOptions) GetJars() []url.URL        { return opts.Jars }
func (opts GatewayOptions) GetLibraryDirs() []url.URL { return opts.LibraryDirs }

func TestOptionsWithEmptyListValues(t *testing.T) {
	opts := GatewayOptions{PrintHelp: false, Port: nil, DefaultConfig: nil, Jars: []url.URL{}, LibraryDirs: []url.URL{}}
	assert.False(t, opts.IsPrintHelp())
	assert.Nil(t, opts.GetPort())
	assert.Nil(t, opts.GetDefaultConfig())
	assert.Equal(t, []url.URL{}, opts.GetJars())
	assert.Equal(t, []url.URL{}, opts.GetLibraryDirs())
}

func TestOptionsWithDifferentValues(t *testing.T) {
	dummyUrl, err := url.Parse("file:/tmp/publictest2.jar")
	assert.NoError(t, err)
	port := 9090
	opts := GatewayOptions{
		PrintHelp:     true,
		Port:          &port,
		DefaultConfig: dummyUrl,
		Jars:          []url.URL{*dummyUrl},
		LibraryDirs:   []url.URL{*dummyUrl},
	}
	assert.True(t, opts.IsPrintHelp())
	assert.Equal(t, 9090, *opts.GetPort())
	assert.NotNil(t, opts.GetDefaultConfig())
	assert.Equal(t, *dummyUrl, *opts.GetDefaultConfig())
	assert.Equal(t, []url.URL{*dummyUrl}, opts.GetJars())
	assert.Equal(t, []url.URL{*dummyUrl}, opts.GetLibraryDirs())
}