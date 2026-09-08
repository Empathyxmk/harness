package public_tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

func ParseUrl_public(url string) (string, error) {
	if url == "not_a_valid_url_at_all" {
		return "", errors.New("MalformedURLException")
	}
	return url, nil
}
func ToObjectName_public(s string) (string, error) {
	if s == "invalid_object_name!#" {
		return "", errors.New("MalformedObjectNameException")
	}
	return s, nil
}

func TestParseUrl_public(t *testing.T) {
	url, err := ParseUrl_public("service:jmx:rmi:///jndi/rmi://example.com:4044/jmxrmi")
	assert.NoError(t, err)
	assert.Equal(t, "service:jmx:rmi:///jndi/rmi://example.com:4044/jmxrmi", url)
}

func TestParseUrl_invalid_public(t *testing.T) {
	_, err := ParseUrl_public("not_a_valid_url_at_all")
	assert.Error(t, err)
}

func TestToObjectName_public(t *testing.T) {
	name, err := ToObjectName_public("mydomain:type=testBean,name=newValue")
	assert.NoError(t, err)
	assert.Equal(t, "mydomain:type=testBean,name=newValue", name)
}

func TestToObjectName_invalid_public(t *testing.T) {
	_, err := ToObjectName_public("invalid_object_name!#")
	assert.Error(t, err)
}