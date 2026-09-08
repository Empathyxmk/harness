package original

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

func TestOptionsWithNulls(t *testing.T) {
	opts := GatewayOptions{PrintHelp: true, Port: nil, DefaultConfig: nil, Jars: nil, LibraryDirs: nil}
	assert.True(t, opts.IsPrintHelp())
	assert.Nil(t, opts.GetPort())
	assert.Nil(t, opts.GetDefaultConfig())
	assert.Equal(t, []url.URL(nil), opts.GetJars())
	assert.Equal(t, []url.URL(nil), opts.GetLibraryDirs())
}

func TestOptionsWithValues(t *testing.T) {
	dummyUrl, err := url.Parse("file:/tmp/test1.jar")
	assert.NoError(t, err)
	port := 8081
	opts := GatewayOptions{
		PrintHelp:     false,
		Port:          &port,
		DefaultConfig: dummyUrl,
		Jars:          []url.URL{*dummyUrl},
		LibraryDirs:   []url.URL{*dummyUrl},
	}
	assert.False(t, opts.IsPrintHelp())
	assert.Equal(t, 8081, *opts.GetPort())
	assert.NotNil(t, opts.GetDefaultConfig())
	assert.Equal(t, *dummyUrl, *opts.GetDefaultConfig())
	assert.Equal(t, []url.URL{*dummyUrl}, opts.GetJars())
	assert.Equal(t, []url.URL{*dummyUrl}, opts.GetLibraryDirs())
}