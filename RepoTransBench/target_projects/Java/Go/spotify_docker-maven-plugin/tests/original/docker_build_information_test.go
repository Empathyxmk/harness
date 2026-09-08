package tests

import (
	"encoding/json"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummyLog struct{}

type DockerBuildInformation struct {
	Image  string `json:"image"`
	Digest string `json:"digest"`
}

func NewDockerBuildInformation(image string, _ DummyLog) *DockerBuildInformation {
	return &DockerBuildInformation{Image: image}
}

func (d *DockerBuildInformation) SetDigest(digest string) {
	d.Digest = digest
}

func (d *DockerBuildInformation) GetImage() string {
	return d.Image
}

func (d *DockerBuildInformation) GetDigest() string {
	return d.Digest
}

func (d *DockerBuildInformation) ToJSONBytes() []byte {
	bytes, _ := json.Marshal(d)
	return bytes
}

func TestDockerBuildInformation_ConstructorAndGetters(t *testing.T) {
	dbi := NewDockerBuildInformation("theImage", DummyLog{})
	assert.Equal(t, "theImage", dbi.GetImage())
	dbi.SetDigest("digestVal")
	assert.Equal(t, "digestVal", dbi.GetDigest())
}

func TestDockerBuildInformation_ToJsonBytes(t *testing.T) {
	dbi := NewDockerBuildInformation("testing", DummyLog{})
	dbi.SetDigest("digest")
	jsonbytes := dbi.ToJSONBytes()
	s := string(jsonbytes)
	assert.Contains(t, s, "\"digest\"")
	assert.Contains(t, s, "\"image\"")
}