package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type testMountainStream struct {
	writelnCalled bool
}

func (s *testMountainStream) writeln(...interface{}) {
	s.writelnCalled = true
}

type testMountainLesson struct {
	learnCalled bool
}

func (l *testMountainLesson) learn(...interface{}) {
	l.learnCalled = true
}

type Mountain struct {
	stream *testMountainStream
	lesson *testMountainLesson
}

func (m *Mountain) walkThePath() {
	// simulate what run would do - call write & learn
	if m.stream != nil {
		m.stream.writeln("walking")
	}
	if m.lesson != nil {
		m.lesson.learn("learn something")
	}
}

func TestMountainGetsTestResults(t *testing.T) {
	m := &Mountain{
		stream: &testMountainStream{},
		lesson: &testMountainLesson{},
	}
	m.walkThePath()
	assert.True(t, m.lesson.learnCalled)
}