package public_tests

import (
	"os"
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

func TestMessageAndContributionsPerDayBoundsPublic(t *testing.T) {
	cleanupRepos(t)
	now := time.Now()
	msg := contribute.Message(now)
	if !contains(msg, "Contr") {
		t.Errorf("Expected 'Contr' in message, got: %s", msg)
	}
	args := contribute.Args{
		MaxCommits: 9999,
	}
	oldRandInt := contribute.RandInt
	contribute.RandInt = func(a, b int) int { return b }
	defer func() { contribute.RandInt = oldRandInt }()
	count := contribute.ContributionsPerDay(args)
	if count != 20 {
		t.Errorf("ContributionsPerDay max bound failed: got %d, want 20", count)
	}
	args2 := contribute.Args{
		MaxCommits: -20,
	}
	count2 := contribute.ContributionsPerDay(args2)
	if count2 != 1 {
		t.Errorf("ContributionsPerDay min bound failed: got %d, want 1", count2)
	}
}

func TestArgumentsAndInvalidArgsPublic(t *testing.T) {
	cleanupRepos(t)
	out, err := contribute.Arguments([]string{
		"--no_weekends", "--max_commits", "9",
		"--frequency", "10", "--days_after", "6",
		"--repository", "repo-test", "--user_name", "Public User",
		"--user_email", "public-user@example.com",
	})
	if err != nil {
		t.Errorf("Expected no error for arguments, but got: %v", err)
	}
	if !out.NoWeekends {
		t.Errorf("Expected .NoWeekends true")
	}
	if out.MaxCommits != 9 {
		t.Errorf("Expected .MaxCommits 9, got %d", out.MaxCommits)
	}
	if out.Frequency != 10 {
		t.Errorf("Expected .Frequency 10, got %d", out.Frequency)
	}
	if out.Repository != "repo-test" {
		t.Errorf("Expected .Repository 'repo-test', got %q", out.Repository)
	}
	if out.UserName != "Public User" {
		t.Errorf("Expected .UserName 'Public User', got %q", out.UserName)
	}
	if out.UserEmail != "public-user@example.com" {
		t.Errorf("Expected .UserEmail 'public-user@example.com', got %q", out.UserEmail)
	}
	if out.DaysAfter != 6 {
		t.Errorf("Expected .DaysAfter 6, got %d", out.DaysAfter)
	}
	// Invalid argument
	_, err = contribute.Arguments([]string{"--notarealarg"})
	if err == nil {
		t.Errorf("Expected error for invalid arg")
	}
}

func TestDatesRangePublic(t *testing.T) {
	minDay, maxDay := 10, 13
	now := time.Now().Truncate(24 * time.Hour)
	start := now.AddDate(0, 0, -minDay)
	end := now.AddDate(0, 0, maxDay)
	out := contribute.DatesRange(start, end)
	if !out[0].Equal(start) {
		t.Errorf("DatesRange start: got %v, want %v", out[0], start)
	}
	if !out[len(out)-1].Equal(end) {
		t.Errorf("DatesRange end: got %v, want %v", out[len(out)-1], end)
	}
	if len(out) != minDay+maxDay+1 {
		t.Errorf("DatesRange len: got %d, want %d", len(out), minDay+maxDay+1)
	}
}

func TestIsWeekendPublic(t *testing.T) {
	sunday := time.Date(2023, 7, 9, 0, 0, 0, 0, time.UTC)   // Sunday
	tuesday := time.Date(2023, 7, 11, 0, 0, 0, 0, time.UTC) // Tuesday
	if !contribute.IsWeekend(sunday) {
		t.Errorf("Expected sunday to be weekend")
	}
	if contribute.IsWeekend(tuesday) {
		t.Errorf("Did not expect tuesday to be weekend")
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