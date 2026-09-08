package original

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "mapio_GraphvizAnim/gvanim"
)

func TestStepCopyAndRepr(t *testing.T) {
    step1 := gvanim.NewStep()
    step1.VAdd(1)
    step1.EAdd([2]int{1, 2})
    step1.LVSet(1, "A")
    step1.LESet([2]int{1, 2}, "EdgeLabel")
    step2 := gvanim.NewStepFrom(step1)
    assert.Equal(t, step1.V(), step2.V(), "vertex sets should be equal")
    assert.Equal(t, step1.E(), step2.E(), "edge sets should be equal")
    assert.Equal(t, step1.LV(), step2.LV(), "vertex labels should be equal")
    assert.Equal(t, step1.LE(), step2.LE(), "edge labels should be equal")
    r := step2.Repr()
    assert.Contains(t, r, "V")
    assert.Contains(t, r, "E")
}

func TestNodeFormatBasic(t *testing.T) {
    s := gvanim.NewStep()
    s.VAdd(1)
    s.LVSet(1, "A")
    s.HVSet(1, "blue")
    res := s.NodeFormat(1)
    assert.Contains(t, res, "label=")
    assert.Contains(t, res, "color=blue")
}

func TestNodeFormatHidden(t *testing.T) {
    s := gvanim.NewStep()
    res := s.NodeFormat(99)
    assert.Contains(t, res, "style=invis")
}

func TestEdgeFormatAll(t *testing.T) {
    s := gvanim.NewStep()
    e := [2]int{1, 2}
    s.EAdd(e)
    s.LESet(e, "lbl")
    s.HESet(e, "green")
    res := s.EdgeFormat(e)
    assert.Contains(t, res, "label=")
    assert.Contains(t, res, "color=green")
}

func TestEdgeFormatHidden(t *testing.T) {
    s := gvanim.NewStep()
    res := s.EdgeFormat([2]int{3, 4})
    assert.Contains(t, res, "style=invis")
}

func TestAnimationActionMethods(t *testing.T) {
    anim := gvanim.NewAnimation()
    anim.NextStep()
    anim.AddNode(1)
    anim.HighlightNode(2, "yellow")
    anim.LabelNode(2, "Y")
    anim.UnlabelNode(2)
    anim.RemoveNode(2)
    anim.AddEdge(1, 3)
    anim.HighlightEdge(1, 3, "green")
    anim.LabelEdge(1, 3, "E")
    anim.UnlabelEdge(1, 3)
    anim.RemoveEdge(1, 3)
    // just check for panic/errors
}

func TestAnimationParseGood(t *testing.T) {
    anim := gvanim.NewAnimation()
    err := anim.Parse([]string{
        "an 7",
        "ae 7 8",
        "ln 7 labelA",
        "le 7 8 labelE",
        "hn 7",
        "he 7 8",
        "ns",
        "un 7",
        "ue 7 8",
        "rn 7",
        "re 7 8",
    })
    assert.NoError(t, err)
}

func TestAnimationParseBad(t *testing.T) {
    anim := gvanim.NewAnimation()
    err := anim.Parse([]string{"foobar 1"})
    assert.Error(t, err)
}

func TestAnimationParseBadFormat(t *testing.T) {
    anim := gvanim.NewAnimation()
    err1 := anim.Parse([]string{"ae 2"})
    err2 := anim.Parse([]string{"an notanint"})
    assert.Error(t, err1)
    assert.Error(t, err2)
}