package original

import (
	"os"
	"path/filepath"
	"testing"
	"time"

	contribute "github.com/example/shpota_github_activity_generator"
)

func cleanupRepos(t *testing.T) {
	entries, err := os.ReadDir(".")
	if err != nil {
		return
	}
	for _, entry := range entries {
		if entry.IsDir() && len(entry.Name()) >= 10 && entry.Name()[:10] == "repository" {
			_ = os.RemoveAll(entry.Name())
		}
	}
}

func TestMessageAndContributionsPerDayBounds(t *testing.T) {
	cleanupRepos(t)
	now := time.Now()
	msg := contribute.Message(now)
	if !contains(msg, "Contribution") {
		t.Errorf("Expected 'Contribution' in message, got: %s", msg)
	}
	// Max commits capped at 20
	args := contribute.Args{
		MaxCommits: 50,
	}
	oldRandInt := contribute.RandInt
	contribute.RandInt = func(a, b int) int { return b }
	defer func() { contribute.RandInt = oldRandInt }()
	count := contribute.ContributionsPerDay(args)
	if count != 20 {
		t.Errorf("ContributionsPerDay max bound failed: got %d (want 20)", count)
	}
	// Min commits floored at 1
	args2 := contribute.Args{
		MaxCommits: -5,
	}
	count2 := contribute.ContributionsPerDay(args2)
	if count2 != 1 {
		t.Errorf("ContributionsPerDay min bound failed: got %d (want 1)", count2)
	}
}

func TestArgumentsAndInvalidArgs(t *testing.T) {
	cleanupRepos(t)
	out, err := contribute.Arguments([]string{
		"--no_weekends", "--max_commits", "4",
		"--frequency", "50", "--days_before", "3",
		"--days_after", "1",
	})
	if err != nil {
		t.Fatalf("Error calling Arguments: %v", err)
	}
	if !out.NoWeekends {
		t.Errorf("Expected .NoWeekends true")
	}
	if out.MaxCommits != 4 {
		t.Errorf("Expected .MaxCommits 4, got %d", out.MaxCommits)
	}
	if out.Frequency != 50 {
		t.Errorf("Expected .Frequency 50, got %d", out.Frequency)
	}
	if out.DaysBefore != 3 {
		t.Errorf("Expected .DaysBefore 3, got %d", out.DaysBefore)
	}
	if out.DaysAfter != 1 {
		t.Errorf("Expected .DaysAfter 1, got %d", out.DaysAfter)
	}
	// Test invalid argument (should error)
	_, err = contribute.Arguments([]string{"--notarealarg"})
	if err == nil {
		t.Errorf("Expected error for invalid argument")
	}
}

// NOTE: You cannot override os.Getwd in real Go code; here we just test logic, not filesystem effects.
func TestRunAndContribute(t *testing.T) {
	cleanupRepos(t)
	var called [][]string
	oldRun := contribute.Run
	contribute.Run = func(cmd []string) error {
		cpy := make([]string, len(cmd))
		copy(cpy, cmd)
		called = append(called, cpy)
		return nil
	}
	defer func() { contribute.Run = oldRun }()
	testDir := t.TempDir()
	// Normally, file output would happen in cwd.
	// To simulate safe file output: change working directory for test scope if possible
	oldWd, _ := os.Getwd()
	_ = os.Chdir(testDir)
	defer os.Chdir(oldWd)
	dt := time.Date(2023, 2, 17, 15, 45, 0, 0, time.UTC)
	if err := contribute.Contribute(dt); err != nil {
		t.Fatalf("Contribute: %v", err)
	}
	readmePath := filepath.Join(testDir, "README.md")
	b, err := os.ReadFile(readmePath)
	if err != nil {
		t.Fatalf("Missing README.md: %v", err)
	}
	content := string(b)
	if !contains(content, "Contribution:") {
		t.Errorf("Expected 'Contribution:' in README.md, got: %s", content)
	}
}

func TestMainMinimal(t *testing.T) {
	cleanupRepos(t)
	oldRun := contribute.Run
	contribute.Run = func([]string) error { return nil }
	defer func() { contribute.Run = oldRun }()
	oldContribute := contribute.Contribute
	contributed := false
	contribute.Contribute = func(time.Time) error {
		contributed = true
		return nil
	}
	defer func() { contribute.Contribute = oldContribute }()
	now := time.Date(2023, 2, 21, 13, 0, 0, 0, time.UTC)
	contribute.SetNowFunc(func() time.Time { return now })
	contribute.RandInt = func(a, b int) int { return 0 }
	args := []string{"--days_before", "1", "--days_after", "1", "--max_commits", "1"}
	contribute.Main(args)
	if !contributed {
		t.Errorf("Contribute did not run")
	}
}

func TestMainWithRepository(t *testing.T) {
	cleanupRepos(t)
	oldRun := contribute.Run
	var calls [][]string
	contribute.Run = func(cmd []string) error {
		cp := make([]string, len(cmd))
		copy(cp, cmd)
		calls = append(calls, cp)
		return nil
	}
	defer func() { contribute.Run = oldRun }()
	oldContribute := contribute.Contribute
	contribute.Contribute = func(time.Time) error { return nil }
	defer func() { contribute.Contribute = oldContribute }()
	now := time.Date(2023, 2, 21, 13, 0, 0, 0, time.UTC)
	contribute.SetNowFunc(func() time.Time { return now })
	contribute.RandInt = func(a, b int) int { return 100 }
	args := []string{
		"--repository", "https://github.com/testuser/somerepo.git",
		"--user_name", "foo", "--user_email", "bar@test.com",
		"--days_before", "1", "--days_after", "1",
	}
	contribute.Main(args)
	var remote, push bool
	for _, c := range calls {
		for _, part := range c {
			if contains(part, "remote") {
				remote = true
			}
			if contains(part, "push") {
				push = true
			}
		}
	}
	if !remote {
		t.Errorf("No git remote command called")
	}
	if !push {
		t.Errorf("No git push command called")
	}
}

func contains(hay, needle string) bool {
	return len(hay) >= len(needle) && (func() bool {
		for i := 0; i+len(needle) <= len(hay); i++ {
			if hay[i:i+len(needle)] == needle {
				return true
			}
		}
		return false
	})()
}