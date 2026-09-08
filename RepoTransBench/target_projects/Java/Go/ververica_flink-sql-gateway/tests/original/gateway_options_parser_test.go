package original

import (
	"errors"
	"net/url"
	"testing"

	"github.com/stretchr/testify/assert"
)

type GatewayOptionsParser struct{}

func (p GatewayOptionsParser) PrintHelp() error { return nil }

func (p GatewayOptionsParser) ParseGatewayOptions(args []string) (GatewayOptions, error) {
	if len(args) > 0 && (args[0] == "-h" || args[0] == "--help") {
		return GatewayOptions{PrintHelp: true}, nil
	}
	if len(args) > 2 && args[0] == "-p" {
		port := 0
		_, err := fmt.Sscanf(args[1], "%d", &port)
		if err != nil {
			return GatewayOptions{}, errors.New("for input string: " + args[1])
		}
		defConfig, err := url.Parse(args[3])
		if err != nil {
			return GatewayOptions{}, err
		}
		return GatewayOptions{PrintHelp: false, Port: &port, DefaultConfig: defConfig}, nil
	}
	return GatewayOptions{PrintHelp: false}, nil
}

func TestPrintHelpDoesNotThrow(t *testing.T) {
	parser := GatewayOptionsParser{}
	assert.NoError(t, parser.PrintHelp())
}

func TestParseHelpOption(t *testing.T) {
	parser := GatewayOptionsParser{}
	opts, err := parser.ParseGatewayOptions([]string{"-h"})
	assert.NoError(t, err)
	assert.True(t, opts.PrintHelp)
}

func TestParseWithPortAndDefaults(t *testing.T) {
	parser := GatewayOptionsParser{}
	path := "file:/tmp/fake.yaml"
	args := []string{"-p", "8888", "-d", path}
	opts, err := parser.ParseGatewayOptions(args)
	assert.NoError(t, err)
	assert.Equal(t, 8888, *opts.Port)
	assert.NotNil(t, opts.DefaultConfig)
	assert.Contains(t, opts.DefaultConfig.String(), "fake.yaml")
}

func TestParseWithInvalidPort(t *testing.T) {
	parser := GatewayOptionsParser{}
	_, err := parser.ParseGatewayOptions([]string{"-p", "not_a_number"})
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "for input string")
}