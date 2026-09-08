package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type RegistryAuth struct {
	Email         string
	Password      string
	Username      string
	ServerAddress string
}

type RegistryAuthSupplier struct {
	configs map[string]RegistryAuth
}

func (rs *RegistryAuthSupplier) AuthForBuild() map[string]RegistryAuth {
	return rs.configs
}
func (rs *RegistryAuthSupplier) AuthFor(image string) RegistryAuth {
	return rs.configs[image]
}

type AbstractDockerMojo struct {
	DockerHost   string
	DockerCert   string
	ServerId     string
	RegistryUrl  string
	authSupplier RegistryAuthSupplier
}

func (a *AbstractDockerMojo) Execute() {
	// just a simulation, here you'd set up docker client
}

func TestDockerHostSet(t *testing.T) {
	sut := &AbstractDockerMojo{
		DockerHost: "testhost", DockerCert: "certs",
	}
	sut.Execute()
	assert.Equal(t, "testhost", sut.DockerHost)
	assert.Equal(t, "certs", sut.DockerCert)
}

func TestAuthorizationConfiguration(t *testing.T) {
	sut := &AbstractDockerMojo{
		ServerId: "testId",
	}
	sut.authSupplier = RegistryAuthSupplier{
		configs: map[string]RegistryAuth{
			"testId": {
				Email:         "user@host.domain",
				Password:      "password",
				Username:      "username",
				ServerAddress: "testId",
			},
		},
	}
	auth := sut.authSupplier.AuthForBuild()["testId"]
	assert.NotNil(t, auth)
	assert.Equal(t, "user@host.domain", auth.Email)
	assert.Equal(t, "password", auth.Password)
	assert.Equal(t, "username", auth.Username)
	assert.Equal(t, "testId", auth.ServerAddress)
}

func TestAuthorizationConfigurationWithServerAddress(t *testing.T) {
	sut := &AbstractDockerMojo{
		ServerId:    "testId",
		RegistryUrl: "my.docker.reg",
	}
	sut.authSupplier = RegistryAuthSupplier{
		configs: map[string]RegistryAuth{
			"my.docker.reg/foo/bar:blah": {
				Email:         "user@host.domain",
				Password:      "password",
				Username:      "username",
				ServerAddress: "my.docker.reg",
			},
		},
	}
	auth := sut.authSupplier.AuthFor("my.docker.reg/foo/bar:blah")
	assert.NotNil(t, auth)
	assert.Equal(t, "user@host.domain", auth.Email)
	assert.Equal(t, "password", auth.Password)
	assert.Equal(t, "username", auth.Username)
	assert.Equal(t, "my.docker.reg", auth.ServerAddress)
}