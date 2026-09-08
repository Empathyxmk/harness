package original

import (
	"testing"

	"jameszbl_java_design_patterns/facade"
)

// An in-memory logger for capturing output (simulate Java's logback+InMemoryAppender)
type inMemoryLogger struct {
	messages []string
}

func (l *inMemoryLogger) log(msg string) {
	l.messages = append(l.messages, msg)
}
func (l *inMemoryLogger) logContains(sub string) bool {
	for _, m := range l.messages {
		if m == sub {
			return true
		}
	}
	return false
}
func (l *inMemoryLogger) getLogSize() int {
	return len(l.messages)
}

func TestCourseFacadeWholeDayOfSchool(t *testing.T) {
	logger := &inMemoryLogger{}
	// Next, inject logger into the facade under test (assume facade supports this pattern)
	f := facade.NewCourseFacadeWithLogger(logger.log)

	// Preparation
	f.Prepare()
	if !logger.logContains("老师赶往学校") {
		t.Error("Teacher should go to school")
	}
	if !logger.logContains("学生赶往学校") {
		t.Error("Student should go to school")
	}
	if !logger.logContains("老师准备上课") {
		t.Error("Teacher should prepare to teach")
	}
	if !logger.logContains("学生准备上课") {
		t.Error("Student should prepare to learn")
	}
	if logger.getLogSize() != 4 {
		t.Errorf("log size after prepare: got %d, want 4", logger.getLogSize())
	}

	// Proceed
	f.Proceed()
	studentLesson := 0
	for _, m := range logger.messages {
		if m == "学生正在上课" {
			studentLesson++
		}
	}
	if studentLesson != 2 || logger.getLogSize() != 6 {
		t.Errorf("log during lesson: got %d student lessons, %d total entries", studentLesson, logger.getLogSize())
	}

	// Stop
	f.Stop()
	if !logger.logContains("学生下课") {
		t.Error("Student should finish class")
	}
	if !logger.logContains("老师下课") {
		t.Error("Teacher should finish class")
	}
	if !logger.logContains("老师回家") {
		t.Error("Teacher should go home")
	}
	if !logger.logContains("学生回家") {
		t.Error("Student should go home")
	}
	if logger.getLogSize() != 10 {
		t.Errorf("log size after finish: got %d, want 10", logger.getLogSize())
	}
}