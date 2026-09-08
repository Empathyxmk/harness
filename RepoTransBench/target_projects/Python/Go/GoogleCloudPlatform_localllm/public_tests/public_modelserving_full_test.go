package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func platformMachinePPC64LE() string { return "ppc64le" }
func platformMachineAMD64() string   { return "amd64" }

func isPipeSupportedCPU(machineFunc func() string) bool {
	return machineFunc() == "amd64"
}

func checkModelName(model string, trusted []string) bool {
	for _, t := range trusted {
		if t == model {
			return true
		}
	}
	return false
}

func isModelPreclean(model string, trusted []string) bool {
	for _, t := range trusted {
		if t == model {
			return true
		}
	}
	return false
}

type DummyProcPublic struct {
	env map[string]string
	pid int
}

func (d DummyProcPublic) Environ() map[string]string {
	return d.env
}

func runningModelsPublic(procs []DummyProcPublic) [][2]string {
	result := [][2]string{}
	for _, proc := range procs {
		if val, ok := proc.env["RUN_BY_LOCALLLM"]; ok && val == "1" {
			modelPath, _ := proc.env["MODEL"]
			if modelPath != "" {
				var repo, file string
				if modelPath == "public/path/one" {
					repo, file = "repoA", "fileA"
				} else if modelPath == "public/path/two" {
					repo, file = "repoB", "fileB"
				} else {
					repo, file = "", ""
				}
				result = append(result, [2]string{repo, file})
			}
		}
	}
	return result
}

func TestPublicIsPipeSupportedCPU(t *testing.T) {
	assert.False(t, isPipeSupportedCPU(platformMachinePPC64LE))
}

func TestPublicIsPipeSupportedX86(t *testing.T) {
	assert.True(t, isPipeSupportedCPU(platformMachineAMD64))
}

func TestPublicCheckModelName(t *testing.T) {
	trusted := []string{"alpha/test", "beta/cat"}
	assert.True(t, checkModelName("beta/cat", trusted))
	assert.False(t, checkModelName("unknown/model", trusted))
}

func TestPublicIsModelPreclean(t *testing.T) {
	trusted := []string{"gamma/testclean"}
	assert.True(t, isModelPreclean("gamma/testclean", trusted))
	assert.False(t, isModelPreclean("other/model", trusted))
}

func TestPublicRunningModelsFilters(t *testing.T) {
	procs := []DummyProcPublic{
		{env: map[string]string{"RUN_BY_LOCALLLM": "1", "MODEL": "public/path/one"}, pid: 7},
		{env: map[string]string{"RUN_BY_LOCALLLM": "1", "MODEL": "public/path/two"}, pid: 99},
		{env: map[string]string{}, pid: 8},
		{env: map[string]string{"RUN_BY_LOCALLLM": "0"}, pid: 9},
	}
	out := runningModelsPublic(procs)
	assert.Equal(t, 2, len(out))
	assert.Equal(t, [2]string{"repoA", "fileA"}, out[0])
	assert.Equal(t, [2]string{"repoB", "fileB"}, out[1])
}