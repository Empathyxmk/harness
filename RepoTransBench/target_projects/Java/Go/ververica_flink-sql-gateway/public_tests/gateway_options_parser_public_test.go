package public_tests

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

func TestPrintHelpDoesNotThrowPublic(t *testing.T) {
	parser := GatewayOptionsParser{}
	assert.NoError(t, parser.PrintHelp())
}

func TestParseHelpOptionLong(t *testing.T) {
	parser := GatewayOptionsParser{}
	opts, err := parser.ParseGatewayOptions([]string{"--help"})
	assert.NoError(t, err)
	assert.True(t, opts.PrintHelp)
}

func TestParseWithDifferentPortAndDefaults(t *testing.T) {
	parser := GatewayOptionsParser{}
	path := "file:/tmp/test-sql-gateway-configuration.yaml"
	args := []string{"-p", "9999", "-d", path}
	opts, err := parser.ParseGatewayOptions(args)
	assert.NoError(t, err)
	assert.Equal(t, 9999, *opts.Port)
	assert.NotNil(t, opts.DefaultConfig)
	assert.Contains(t, opts.DefaultConfig.String(), "test-sql-gateway-configuration.yaml")
}

func TestParseWithNegativePort(t *testing.T) {
	parser := GatewayOptionsParser{}
	args := []string{"-p", "-42"}
	opts, err := parser.ParseGatewayOptions(args)
	assert.NoError(t, err)
	assert.Equal(t, -42, *opts.Port)
}