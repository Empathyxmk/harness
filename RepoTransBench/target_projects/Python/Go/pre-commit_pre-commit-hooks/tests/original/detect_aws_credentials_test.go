package original

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"precommit_hooks"
)

func TestGetAwsCredentialsFileFromEnv(t *testing.T) {
	testCases := []struct {
		envVars map[string]string
		values  map[string]struct{}
	}{
		{map[string]string{}, map[string]struct{}{}},
		{map[string]string{"AWS_PLACEHOLDER_KEY": "/foo"}, map[string]struct{}{}},
		{map[string]string{"AWS_CONFIG_FILE": "/foo"}, map[string]struct{}{"/foo": {}}},
		{map[string]string{"AWS_CREDENTIAL_FILE": "/foo"}, map[string]struct{}{"/foo": {}}},
		{map[string]string{"AWS_SHARED_CREDENTIALS_FILE": "/foo"}, map[string]struct{}{"/foo": {}}},
		{map[string]string{"BOTO_CONFIG": "/foo"}, map[string]struct{}{"/foo": {}}},
		{map[string]string{"AWS_PLACEHOLDER_KEY": "/foo", "AWS_CONFIG_FILE": "/bar"}, map[string]struct{}{"/bar": {}}},
		{
			map[string]string{"AWS_PLACEHOLDER_KEY": "/foo", "AWS_CONFIG_FILE": "/bar", "AWS_CREDENTIAL_FILE": "/baz"},
			map[string]struct{}{"/bar": {}, "/baz": {}},
		},
		{
			map[string]string{"AWS_CONFIG_FILE": "/foo", "AWS_CREDENTIAL_FILE": "/bar", "AWS_SHARED_CREDENTIALS_FILE": "/baz"},
			map[string]struct{}{"/foo": {}, "/bar": {}, "/baz": {}},
		},
	}
	for _, tc := range testCases {
		oldEnv := saveAndSetEnv(tc.envVars)
		got := precommit_hooks.GetAwsCredFilesFromEnv()
		assert.True(t, compareStringSet(got, tc.values))
		restoreEnv(oldEnv)
	}
}

func TestGetAwsSecretsFromEnv(t *testing.T) {
	testCases := []struct {
		envVars map[string]string
		values  map[string]struct{}
	}{
		{map[string]string{}, map[string]struct{}{}},
		{map[string]string{"AWS_PLACEHOLDER_KEY": "foo"}, map[string]struct{}{}},
		{map[string]string{"AWS_SECRET_ACCESS_KEY": "foo"}, map[string]struct{}{"foo": {}}},
		{map[string]string{"AWS_SECURITY_TOKEN": "foo"}, map[string]struct{}{"foo": {}}},
		{map[string]string{"AWS_SESSION_TOKEN": "foo"}, map[string]struct{}{"foo": {}}},
		{map[string]string{"AWS_SESSION_TOKEN": ""}, map[string]struct{}{}},
		{map[string]string{"AWS_SESSION_TOKEN": "foo", "AWS_SECURITY_TOKEN": ""}, map[string]struct{}{"foo": {}}},
		{
			map[string]string{"AWS_PLACEHOLDER_KEY": "foo", "AWS_SECRET_ACCESS_KEY": "bar"},
			map[string]struct{}{"bar": {}},
		},
		{
			map[string]string{"AWS_SECRET_ACCESS_KEY": "foo", "AWS_SECURITY_TOKEN": "bar"},
			map[string]struct{}{"foo": {}, "bar": {}},
		},
	}
	for _, tc := range testCases {
		oldEnv := saveAndSetEnv(tc.envVars)
		got := precommit_hooks.GetAwsSecretsFromEnv()
		assert.True(t, compareStringSet(got, tc.values))
		restoreEnv(oldEnv)
	}
}

func TestGetAwsSecretsFromFile(t *testing.T) {
	tmp := getResourceDir()
	testCases := []struct {
		filename      string
		expected_keys map[string]struct{}
	}{
		{"aws_config_with_secret.ini", map[string]struct{}{"z2rpgs5uit782eapz5l1z0y2lurtsyyk6hcfozlb": {}}},
		{"aws_config_with_session_token.ini", map[string]struct{}{"foo": {}}},
		{"aws_config_with_secret_and_session_token.ini", map[string]struct{}{"z2rpgs5uit782eapz5l1z0y2lurtsyyk6hcfozlb": {}, "foo": {}}},
		{"aws_config_with_multiple_sections.ini", map[string]struct{}{"z2rpgs5uit782eapz5l1z0y2lurtsyyk6hcfozlb": {}, "7xebzorgm5143ouge9gvepxb2z70bsb2rtrh099e": {}, "ixswosj8gz3wuik405jl9k3vdajsnxfhnpui38ez": {}, "foo": {}}},
		{"aws_config_without_secrets.ini", map[string]struct{}{}},
		{"aws_config_without_secrets_with_spaces.ini", map[string]struct{}{}},
		{"nonsense.txt", map[string]struct{}{}},
		{"ok_json.json", map[string]struct{}{}},
	}
	for _, tc := range testCases {
		filename := filepath.Join(tmp, tc.filename)
		got := precommit_hooks.GetAwsSecretsFromFile(filename)
		assert.True(t, compareStringSet(got, tc.expected_keys))
	}
}

func TestDetectAwsCredentials(t *testing.T) {
	tmp := getResourceDir()
	testCases := []struct {
		filename        string
		expected_retval int
	}{
		{"aws_config_with_secret.ini", 1},
		{"aws_config_with_session_token.ini", 1},
		{"aws_config_with_multiple_sections.ini", 1},
		{"aws_config_without_secrets.ini", 0},
		{"aws_config_without_secrets_with_spaces.ini", 0},
		{"nonsense.txt", 0},
		{"ok_json.json", 0},
	}
	credentialsFile := filepath.Join(tmp, "aws_config_with_multiple_sections.ini")
	for _, tc := range testCases {
		filename := filepath.Join(tmp, tc.filename)
		code := precommit_hooks.MainDetectAwsCredentials([]string{filename, "--credentials-file", credentialsFile})
		assert.Equal(t, tc.expected_retval, code)
	}
}

func TestAllowsArbitrarilyEncodedFiles(t *testing.T) {
	dir, err := ioutil.TempDir("", "awscreds")
	assert.NoError(t, err)
	defer os.RemoveAll(dir)

	srcIni := filepath.Join(dir, "src.ini")
	err = ioutil.WriteFile(srcIni, []byte("[default]\naws_access_key_id=AKIASDFASDF\naws_secret_Access_key=9018asdf23908190238123\n"), 0644)
	assert.NoError(t, err)

	arb := filepath.Join(dir, "f")
	err = ioutil.WriteFile(arb, []byte{0x12, 0x9a, 0xe2, 0xf2}, 0644)
	assert.NoError(t, err)
	ret := precommit_hooks.MainDetectAwsCredentials([]string{arb, "--credentials-file", srcIni})
	assert.Equal(t, 0, ret)
}

func TestNonExistentCredentials(t *testing.T) {
	restore, called_env, called_file := patchAwsSecretsLookup(
		func() map[string]struct{} { return map[string]struct{}{} },
		func(string) map[string]struct{} { return map[string]struct{}{} },
	)
	defer restore()
	tmp := getResourceDir()
	filename := filepath.Join(tmp, "aws_config_without_secrets.ini")
	code, output := runMainDetectAwsCredentialsCapture([]string{
		filename, "--credentials-file=testing/resources/credentailsfilethatdoesntexist",
	})
	assert.Equal(t, 2, code)
	expect := "No AWS keys were found in the configured credential files and environment variables.\nPlease ensure you have the correct setting for --credentials-file\n"
	assert.Equal(t, expect, output)
	assert.True(t, *called_env && *called_file)
}

func TestNonExistentCredentialsWithAllowFlag(t *testing.T) {
	restore, called_env, called_file := patchAwsSecretsLookup(
		func() map[string]struct{} { return map[string]struct{}{} },
		func(string) map[string]struct{} { return map[string]struct{}{} },
	)
	defer restore()
	tmp := getResourceDir()
	filename := filepath.Join(tmp, "aws_config_without_secrets.ini")
	code := precommit_hooks.MainDetectAwsCredentials([]string{
		filename, "--credentials-file=testing/resources/credentailsfilethatdoesntexist", "--allow-missing-credentials",
	})
	assert.Equal(t, 0, code)
	assert.True(t, *called_env && *called_file)
}

// --- Helpers ---
// You must implement these helpers if using this test file in a real Go package.

func saveAndSetEnv(envVars map[string]string) map[string]string {
	orig := map[string]string{}
	for k := range envVars {
		orig[k] = os.Getenv(k)
		os.Setenv(k, envVars[k])
	}
	return orig
}

func restoreEnv(envVars map[string]string) {
	for k, v := range envVars {
		os.Setenv(k, v)
	}
}

func compareStringSet(a, b map[string]struct{}) bool {
	if len(a) != len(b) {
		return false
	}
	for k := range a {
		if _, ok := b[k]; !ok {
			return false
		}
	}
	return true
}

func getResourceDir() string {
	// Return the directory containing test resources, e.g., "./testing/resources"
	dir := os.Getenv("PRECOMMIT_TEST_RESOURCES")
	if dir != "" {
		return dir
	}
	// fallback (user should override in build env)
	return "./testing/resources"
}

// Patch the secret lookup functions in main for mocking (manual setup required).
func patchAwsSecretsLookup(
	envfunc func() map[string]struct{},
	filefunc func(string) map[string]struct{},
) (restore func(), env_called *bool, file_called *bool) {
	called_env, called_file := false, false
	origEnv := precommit_hooks.GetAwsSecretsFromEnv
	origFile := precommit_hooks.GetAwsSecretsFromFile

	precommit_hooks.GetAwsSecretsFromEnv = func() map[string]struct{} {
		called_env = true
		return envfunc()
	}
	precommit_hooks.GetAwsSecretsFromFile = func(fname string) map[string]struct{} {
		called_file = true
		return filefunc(fname)
	}
	restoreFunc := func() {
		precommit_hooks.GetAwsSecretsFromEnv = origEnv
		precommit_hooks.GetAwsSecretsFromFile = origFile
	}
	return restoreFunc, &called_env, &called_file
}

// Run main and capture stdout
func runMainDetectAwsCredentialsCapture(args []string) (int, string) {
	// redirect os.Stdout for test
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w
	code := precommit_hooks.MainDetectAwsCredentials(args)
	w.Close()
	var buf bytes.Buffer
	_, _ = buf.ReadFrom(r)
	os.Stdout = old
	return code, buf.String()
}