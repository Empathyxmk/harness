package public_tests

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"gopkg.in/yaml.v3"
)

// DummyMaestroException is used for simulation.
type DummyMaestroException struct {
	msg string
}

func (e DummyMaestroException) Error() string { return e.msg }

// Simulates loading services from a YAML file, substitution and failure cases
func loadServicesFromFile(filename string) (map[string]map[string]interface{}, error) {
	if filepath.Ext(filename) == ".txt" {
		return nil, DummyMaestroException{"Unsupported file format"}
	}
	if _, err := os.Stat(filename); err != nil {
		return nil, DummyMaestroException{"File not found"}
	}
	content, err := os.ReadFile(filename)
	if err != nil {
		return nil, DummyMaestroException{"File not found"}
	}
	var data map[string]map[string]interface{}
	if err := yaml.Unmarshal(content, &data); err != nil {
		return nil, DummyMaestroException{"Invalid YAML"}
	}
	// Simulate env var substitution in `environment`
	for _, conf := range data {
		if envList, ok := conf["environment"].([]interface{}); ok {
			newEnv := make([]string, 0, len(envList))
			for _, v := range envList {
				vs, _ := v.(string)
				if idx := strings.Index(vs, "${"); idx != -1 {
					varName := extractVarName(vs)
					val := os.Getenv(varName)
					prefix := vs[:strings.Index(vs, "=")]
					newEnv = append(newEnv, fmt.Sprintf("%s=%s", prefix, val))
				} else {
					newEnv = append(newEnv, vs)
				}
			}
			envVal := make([]interface{}, len(newEnv))
			for i, nv := range newEnv {
				envVal[i] = nv
			}
			conf["environment"] = envVal
		}
	}
	return data, nil
}
func extractVarName(s string) string {
	start := strings.Index(s, "${")
	if start == -1 {
		return ""
	}
	start += 2
	end := strings.Index(s[start:], "}")
	if end == -1 {
		return ""
	}
	return s[start : start+end]
}

func TestLoadInvalidFileExtension(t *testing.T) {
	_, err := loadServicesFromFile("invalid_format.txt")
	assert.Error(t, err)
}

func TestLoadMissingFile(t *testing.T) {
	_, err := loadServicesFromFile("this_file_does_not_exist_public.yaml")
	assert.Error(t, err)
}

func TestLoadEnvVariableSubstitutionPublic(t *testing.T) {
	tmpDir := t.TempDir()
	filename := filepath.Join(tmpDir, "service_env_public.yaml")
	content := `
serviceA:
  image: "public_image:tag"
  environment:
    - PUBLIC_VAR=${PUBLIC_VAR_TEST}
`
	err := os.WriteFile(filename, []byte(content), 0644)
	assert.NoError(t, err)
	os.Setenv("PUBLIC_VAR_TEST", "public_test_value")
	conf, err := loadServicesFromFile(filename)
	assert.NoError(t, err)
	service, ok := conf["serviceA"]
	assert.True(t, ok)
	envIface, ok := service["environment"].([]interface{})
	assert.True(t, ok)
	assert.Equal(t, "PUBLIC_VAR=public_test_value", envIface[0])
}

func TestLoadInvalidYamlSyntax(t *testing.T) {
	tmpDir := t.TempDir()
	filename := filepath.Join(tmpDir, "broken_config_public.yaml")
	content := `
serviceB:
  image: "repo/image
  environment:
    - INVALID
` // Missing closing quote
	err := os.WriteFile(filename, []byte(content), 0644)
	assert.NoError(t, err)
	_, err = loadServicesFromFile(filename)
	assert.Error(t, err)
}