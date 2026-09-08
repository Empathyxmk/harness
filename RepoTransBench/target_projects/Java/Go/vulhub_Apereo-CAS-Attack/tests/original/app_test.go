package original_test

import (
	"bytes"
	"os"
	"strings"
	"testing"

	"apereo-cas-attack/casattack"
)

func captureOutput(f func()) string {
	old := os.Stdout
	r, w, _ := os.Pipe()
	os.Stdout = w

	f()

	w.Close()
	os.Stdout = old
	var buf bytes.Buffer
	_, _ = buf.ReadFrom(r)
	return buf.String()
}

func TestMainNoArgs(t *testing.T) {
	output := captureOutput(func() {
		casattack.Main([]string{})
	})
	if !strings.Contains(output, "Hello from Apereo CAS Attack tool!") {
		t.Errorf("Output did not contain welcome message: %+q", output)
	}
}

func TestMainAttackCasTarget(t *testing.T) {
	output := captureOutput(func() {
		casattack.Main([]string{"attack", "cas-server"})
	})
	if !strings.Contains(output, "Simulating CAS attack on cas-server") {
		t.Errorf("Output did not contain CAS attack message: %+q", output)
	}
}

func TestMainAttackNonCasTarget(t *testing.T) {
	output := captureOutput(func() {
		casattack.Main([]string{"attack", "notcas"})
	})
	if !strings.Contains(output, "Simulating CAS attack on notcas") {
		t.Errorf("Output did not contain CAS attack message for 'notcas': %+q", output)
	}
}

func TestMainAttackNoTarget(t *testing.T) {
	output := captureOutput(func() {
		casattack.Main([]string{"attack"})
	})
	if !strings.Contains(output, "No target specified for attack.") {
		t.Errorf("Output did not contain missing target message: %+q", output)
	}
}

func TestMainHelp(t *testing.T) {
	output := captureOutput(func() {
		casattack.Main([]string{"help"})
	})
	if !strings.Contains(output, "Usage: java -jar apereo-cas-attack.jar") {
		t.Errorf("Output did not contain help usage: %+q", output)
	}
}

func TestMainUnknownCommand(t *testing.T) {
	output := captureOutput(func() {
		casattack.Main([]string{"unknown"})
	})
	if !strings.Contains(output, "Unknown command: unknown") {
		t.Errorf("Output did not contain unknown command message: %+q", output)
	}
	if !strings.Contains(output, "Usage: java -jar apereo-cas-attack.jar") {
		t.Errorf("Output did not contain help usage message: %+q", output)
	}
}

func TestPerformAttackNull(t *testing.T) {
	got := casattack.PerformAttack("")
	want := "No target specified for attack."
	if got != want {
		t.Errorf("PerformAttack(\"\") = %q, want %q", got, want)
	}
}

func TestPerformAttackCasTarget(t *testing.T) {
	got := casattack.PerformAttack("cas-server")
	want := "Simulating CAS attack on cas-server"
	if got != want {
		t.Errorf("PerformAttack(\"cas-server\") = %q, want %q", got, want)
	}
}

func TestPerformAttackNonCasTarget(t *testing.T) {
	got := casattack.PerformAttack("something")
	want := "Target is not a CAS server: something"
	if got != want {
		t.Errorf("PerformAttack(\"something\") = %q, want %q", got, want)
	}
}

func TestPerformAttackCasSubstringCaseInsensitive(t *testing.T) {
	got := casattack.PerformAttack("bestcASattack")
	want := "Target is not a CAS server: bestcASattack"
	if got != want {
		t.Errorf("PerformAttack(\"bestcASattack\") = %q, want %q", got, want)
	}
}