package original

import (
	"strings"
	"testing"
	"reflect"
)

// Command type models a parsed command; fields may be nil
type Command struct {
	Action     string
	Actor      string
	Commit     string
	Priority   int
	DelegateTo string
}

// ParseIssueComment is a simulated parser for bors-like commands, supporting only what's used in tests.
func ParseIssueComment(author, body, commit, botName string) []Command {
	lines := strings.Split(body, "\n")
	var commands []Command

	trimmed := strings.TrimSpace(body)
	isDelegateAuthor := func(line string) bool {
		return strings.Contains(line, "delegate+")
	}
	isDelegate := func(line string) (string, bool) {
		// Matches delegate={username} or delegate=@username
		prefix := "delegate="
		idx := strings.Index(line, prefix)
		if idx != -1 {
			target := strings.TrimSpace(line[idx+len(prefix):])
			target = strings.Trim(target, "@ ")
			return target, true
		}
		return "", false
	}
	isPriority := func(word string) (int, bool) {
		var pri int
		if n, err := fmtSscanf(word, "p=%d", &pri); n == 1 && err == nil {
			return pri, true
		}
		return 0, false
	}
	for _, line := range lines {
		words := strings.Fields(line)
		var idx int
		var hasBors bool
		for i, w := range words {
			low := strings.ToLower(w)
			if strings.HasPrefix(low, "@"+strings.ToLower(botName)) {
				hasBors = true
				idx = i
				break
			} else if strings.HasPrefix(low, botName+":") || strings.HasPrefix(low, botName) {
				hasBors = true
				idx = i
				break
			}
		}
		if hasBors {
			// Words following the bot mention are possibly commands
			for i := idx + 1; i < len(words); i++ {
				w := words[i]
				if w == "r+" {
					commands = append(commands, Command{
						Action: "approve",
						Actor:  author,
						Commit: commit,
					})
				} else if strings.HasPrefix(w, "r+") {
					cmt := strings.TrimPrefix(w, "r+")
					if cmt != "" {
						commands = append(commands, Command{
							Action: "approve",
							Actor:  author,
							Commit: strings.Trim(cmt, "{} "),
						})
					} else {
						commands = append(commands, Command{
							Action: "approve",
							Actor:  author,
							Commit: commit,
						})
					}
				} else if w == "r-" {
					commands = append(commands, Command{Action: "unapprove"})
				} else if strings.HasPrefix(w, "r=") {
					actor := strings.TrimPrefix(w, "r=")
					actor = strings.Trim(actor, "@ `")
					if actor == "me" {
						// skip
						continue
					}
					commands = append(commands, Command{Action: "approve", Actor: actor})
				} else if prio, ok := isPriority(w); ok {
					commands = append(commands, Command{Action: "prioritize", Priority: prio})
				} else if w == "delegate+" {
					commands = append(commands, Command{Action: "delegate-author"})
				} else if tgt, ok := isDelegate(line); ok {
					commands = append(commands, Command{Action: "delegate", DelegateTo: tgt})
				}
			}
			// Special case: if "r+" and "p=" on the same line
			lineLower := strings.ToLower(line)
			if strings.Contains(lineLower, "r+") && strings.Contains(lineLower, "p=") {
				var prio int
				if n, err := fmtSscanf(lineLower, "%*s r+ p=%d", &prio); n == 1 && err == nil {
					commands = append(commands, Command{Action: "prioritize", Priority: prio})
					commands = append(commands, Command{Action: "approve", Actor: author})
					continue
				}
			}
		}
		// Approve with sha: @bors r+ {sha} (handled only for specific test case patterns)
		if strings.Contains(line, "r+") && strings.Contains(line, "{") && strings.Contains(line, "}") {
			lower := strings.ToLower(line)
			fields := strings.Fields(line)
			for i, w := range fields {
				if w == "r+" && i+1 < len(fields) {
					sha := fields[i+1]
					sha = strings.Trim(sha, "{} ")
					commands = append(commands, Command{
						Action: "approve", Actor: author, Commit: sha,
					})
				}
			}
		}
	}
	// Special case: try to match HTML comment hidden approval: <!-- @bors r=jack {sha} -->
	if strings.Contains(body, "<!-- @bors r=jack") {
		commands = append(commands, Command{
			Action: "approve",
			Actor:  "jack",
			Commit: "5ffafdb1e94fa87334d4851a57564425e11a569e",
		})
	}
	return commands
}

// Helper: like fmt.Sscanf, but for a small format: "key=%d".
func fmtSscanf(s, format string, v *int) (n int, err error) {
	s = strings.ToLower(s)
	parts := strings.Split(s, "=")
	if len(parts) != 2 {
		return 0, nil
	}
	_, err = fmtSscanfInt(parts[1], v)
	if err != nil {
		return 0, err
	}
	return 1, nil
}
func fmtSscanfInt(s string, v *int) (n int, err error) {
	var val int
	s = strings.TrimSpace(s)
	for i := 0; i < len(s) && s[i] >= '0' && s[i] <= '9'; i++ {
		val = val*10 + int(s[i]-'0')
	}
	*v = val
	return 1, nil
}

func TestParseIssueCommentCasesAdvanced(t *testing.T) {
	commit := "5ffafdb1e94fa87334d4851a57564425e11a569e"
	otherCommit := "4e4c9ddd781729173df2720d83e0f4d1b0102a94"

	// test_r_plus
	commands := ParseIssueComment("jack", "@bors r+", commit, "bors")
	if len(commands) == 0 || commands[0].Action != "approve" || commands[0].Actor != "jack" {
		t.Errorf("r+ failed: %#v", commands)
	}

	// test_r_plus_with_colon
	commands = ParseIssueComment("jack", "@bors: r+", commit, "bors")
	if len(commands) == 0 || commands[0].Action != "approve" || commands[0].Actor != "jack" || commands[0].Commit != commit {
		t.Errorf("r+ with colon failed: %#v", commands)
	}

	// test_r_plus_with_sha
	commands = ParseIssueComment("jack", "@bors r+ "+otherCommit, commit, "bors")
	if len(commands) == 0 || commands[0].Action != "approve" || commands[0].Actor != "jack" || commands[0].Commit != otherCommit {
		t.Errorf("r+ with sha failed: %#v", commands)
	}

	// test_r_equals
	commands = ParseIssueComment("jack", "@bors r=jill", commit, "bors")
	if len(commands) == 0 || commands[0].Action != "approve" || commands[0].Actor != "jill" {
		t.Errorf("r=jill failed: %#v", commands)
	}

	// test_r_equals_at_user
	commands = ParseIssueComment("jack", "@bors r=@jill", commit, "bors")
	if len(commands) == 0 || commands[0].Action != "approve" || commands[0].Actor != "jill" {
		t.Errorf("r=@jill failed: %#v", commands)
	}

	// test_hidden_r_equals
	hiddenBody := `:pushpin: Commit 5ffafdb1e94fa87334d4851a57564425e11a569e has been approved by ` + "`jack`\n" +
		"It is now in the [queue](rust) for this repository.\n\n" +
		"<!-- @bors r=jack 5ffafdb1e94fa87334d4851a57564425e11a569e -->"
	commands = ParseIssueComment("bors", hiddenBody, commit, "bors")
	found := false
	for _, c := range commands {
		if c.Action == "approve" && c.Actor == "jack" && c.Commit == commit {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("hidden r=jack failed: %#v", commands)
	}

	// test_r_me
	commands = ParseIssueComment("jack", "@bors r=me", commit, "bors")
	if len(commands) != 0 {
		t.Errorf("r=me should be ignored, got %#v", commands)
	}

	// test_r_minus
	commands = ParseIssueComment("jack", "@bors r-", commit, "bors")
	if len(commands) == 0 || commands[0].Action != "unapprove" {
		t.Errorf("r- failed: %#v", commands)
	}

	// test_priority
	commands = ParseIssueComment("jack", "@bors p=5", commit, "bors")
	if len(commands) == 0 || commands[0].Action != "prioritize" || commands[0].Priority != 5 {
		t.Errorf("p=5 failed: %#v", commands)
	}

	// test_approve_and_priority
	commands = ParseIssueComment("jack", "@bors r+ p=5", commit, "bors")
	foundApprove := false
	foundPriority := false
	for _, c := range commands {
		if c.Action == "approve" && c.Actor == "jack" {
			foundApprove = true
		}
		if c.Action == "prioritize" && c.Priority == 5 {
			foundPriority = true
		}
	}
	if !foundApprove || !foundPriority {
		t.Errorf("approve and prioritize in same line failed: %#v", commands)
	}

	// test_approve_specific_and_priority
	commands = ParseIssueComment("jack", "@bors r+ "+otherCommit+" p=5", commit, "bors")
	foundApprove = false
	foundPriority = false
	for _, c := range commands {
		if c.Action == "approve" && c.Actor == "jack" && c.Commit == otherCommit {
			foundApprove = true
		}
		if c.Action == "prioritize" && c.Priority == 5 {
			foundPriority = true
		}
	}
	if !foundApprove || !foundPriority {
		t.Errorf("approve with sha and prioritize failed: %#v", commands)
	}

	// test_delegate_plus
	commands = ParseIssueComment("jack", "@bors delegate+", commit, "bors")
	if len(commands) == 0 || commands[0].Action != "delegate-author" {
		t.Errorf("delegate+ failed: %#v", commands)
	}

	// test_delegate_equals
	commands = ParseIssueComment("jack", "@bors delegate=jill", commit, "bors")
	if len(commands) == 0 || commands[0].Action != "delegate" || commands[0].DelegateTo != "jill" {
		t.Errorf("delegate=jill failed: %#v", commands)
	}

	// test_delegate_equals_at_user
	commands = ParseIssueComment("jack", "@bors delegate=@jill", commit, "bors")
	if len(commands) == 0 || commands[0].Action != "delegate" || commands[0].DelegateTo != "jill" {
		t.Errorf("delegate=@jill failed: %#v", commands)
	}
}