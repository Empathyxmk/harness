package public_tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type MockRepo struct {
	resolveHead func(ref string) (string, error)
}
func (m *MockRepo) Resolve(ref string) (string, error) {
	return m.resolveHead(ref)
}

type Git struct {
	repo *MockRepo
}

func (g *Git) SetRepo(repo *MockRepo) {
	g.repo = repo
}

func (g *Git) GetCommitId() (string, error) {
	if g.repo == nil {
		return "", errors.New("MojoExecutionException")
	}
	val, _ := g.repo.Resolve("HEAD")
	if val == "" {
		return "", nil
	}
	return val, nil
}

func TestGit_GetCommitId_WhenRepoStillNull_ThrowsException(t *testing.T) {
	g := &Git{}
	g.SetRepo(nil)
	_, err := g.GetCommitId()
	assert.Error(t, err)
}

func TestGit_GetCommitId_WhenHeadIsMissing_ReturnsNull(t *testing.T) {
	mockRepo := &MockRepo{
		resolveHead: func(ref string) (string, error) {
			return "", nil
		},
	}
	g := &Git{}
	g.SetRepo(mockRepo)
	commitId, err := g.GetCommitId()
	assert.NoError(t, err)
	assert.Equal(t, "", commitId)
}