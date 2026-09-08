package public_tests

import (
	"bytes"
	"strings"
	"testing"

	"cybereason_logout4shell/tests"
)

func TestLog4jDefaultRunPublic(t *testing.T) {
	var out bytes.Buffer
	log4j := &tests.Log4j{}
	log4j.Main([]string{}, &out)

	result := out.String()
	if !strings.Contains(result, "${jndi:ldap://127.0.0.1:1389/a}") {
		t.Fatalf("Public: Expected JNDI payload in default output, got: %s", result)
	}
}

func TestLog4jThreadContextPublic(t *testing.T) {
	var out bytes.Buffer
	log4j := &tests.Log4j{}
	args := []string{"-t"}
	log4j.Main(args, &out)
	result := out.String()

	if !strings.Contains(result, "Will use ThreadContext as attack vector") {
		t.Errorf("Public: Expected ThreadContext attack vector info, got: %s", result)
	}

	if !strings.Contains(result, "[ATTACK_HEADER] Vulnerable through thread context - 1") {
		t.Errorf("Public: Expected ThreadContext error line 1, got: %s", result)
	}

	if !strings.Contains(result, "[ATTACK_HEADER] Vulnerable through thread context - 2") {
		t.Errorf("Public: Expected ThreadContext error line 2, got: %s", result)
	}
}