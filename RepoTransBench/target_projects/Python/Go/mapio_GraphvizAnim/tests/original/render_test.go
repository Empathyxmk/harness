package original

import (
    "os"
    "testing"
    "github.com/stretchr/testify/assert"
    "mapio_GraphvizAnim/gvanim/render"
    "path/filepath"
)

type dummyPipe struct{}

func (d dummyPipe) Communicate(input []byte) (a, b []byte) { return nil, nil }

type dummyPopen struct{}

func (d dummyPopen) Communicate(input []byte) (a, b []byte) { return nil, nil }

func TestRenderTmp(t *testing.T) {
    // Monkeypatches/workarounds assumed provided via build tags or manual patching if needed.
    // For this translation, we demonstrate structural equivalence.
    tmpDir := t.TempDir()
    // Prepare dummy graphs
    files, err := render.Render([]string{"digraph{}", "digraph{}"}, filepath.Join(tmpDir, "myanim"), "dot", 10)
    assert.NoError(t, err)
    assert.Equal(t, 2, len(files))
    for _, file := range files {
        _, err := os.Stat(file)
        assert.NoError(t, err)
    }
}

func TestGif(t *testing.T) {
    tmpDir := t.TempDir()
    files := []string{}
    for i := 0; i < 2; i++ {
        f := filepath.Join(tmpDir, "f%d.png")
        err := os.WriteFile(f, []byte("test"), 0644)
        assert.NoError(t, err)
        files = append(files, f)
    }
    var called [][]string
    render.SetCallFunc(func(args ...string) error {
        called = append(called, args)
        return nil
    })
    err := render.Gif(files, filepath.Join(tmpDir, "anim"), 123, 11)
    assert.NoError(t, err)
    convertFound := false
    for _, c := range called {
        for _, arg := range c {
            if arg == "convert" {
                convertFound = true
            }
        }
    }
    assert.True(t, convertFound, "should call convert command")
}