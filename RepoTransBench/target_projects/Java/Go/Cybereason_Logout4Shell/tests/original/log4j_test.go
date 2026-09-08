package original

import (
	"bytes"
	"strings"
	"testing"

	"cybereason_logout4shell/tests"
)

func TestDefaultRunPrintsJndiPayload(t *testing.T) {
	var out bytes.Buffer
	log4j := &tests.Log4j{}
	log4j.Main([]string{}, &out)

	result := out.String()
	if !strings.Contains(result, "${jndi:ldap://127.0.0.1:1389/a}") {
		t.Errorf("Expected JNDI payload in output, got: %s", result)
	}
}

func TestThreadContextHeaderAttackVector(t *testing.T) {
	var out bytes.Buffer
	log4j := &tests.Log4j{}

	args := []string{"-t"}
	log4j.Main(args, &out)
	result := out.String()

	if !strings.Contains(result, "Will use ThreadContext as attack vector") {
		t.Errorf("Expected info about ThreadContext attack vector, got: %s", result)
	}

	if !strings.Contains(result, "[ATTACK_HEADER] Vulnerable through thread context - 1") {
		t.Errorf("Expected ThreadContext header error line 1, got: %s", result)
	}

	if !strings.Contains(result, "[ATTACK_HEADER] Vulnerable through thread context - 2") {
		t.Errorf("Expected ThreadContext header error line 2, got: %s", result)
	}
}