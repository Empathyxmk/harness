package public_tests

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "mapio_GraphvizAnim/gvanim"
)

func TestStepCopyAndReprPublic(t *testing.T) {
    step1 := gvanim.NewStep()
    step1.VAdd(10)
    step1.EAdd([2]int{10, 20})
    step1.LVSet(10, "X")
    step1.LESet([2]int{10, 20}, "EdgeAB")
    step2 := gvanim.NewStepFrom(step1)
    assert.Equal(t, step1.V(), step2.V())
    assert.Equal(t, step1.E(), step2.E())
    assert.Equal(t, step1.LV(), step2.LV())
    assert.Equal(t, step1.LE(), step2.LE())
    r := step2.Repr()
    assert.Contains(t, r, "V")
    assert.Contains(t, r, "E")
}

func TestNodeFormatBasicPublic(t *testing.T) {
    s := gvanim.NewStep()
    s.VAdd(5)
    s.LVSet(5, "B")
    s.HVSet(5, "red")
    res := s.NodeFormat(5)
    assert.Contains(t, res, "label=")
    assert.Contains(t, res, "color=red")
}

func TestNodeFormatHiddenPublic(t *testing.T) {
    s := gvanim.NewStep()
    res := s.NodeFormat(123)
    assert.Contains(t, res, "style=invis")
}

func TestEdgeFormatAllPublic(t *testing.T) {
    s := gvanim.NewStep()
    e := [2]int{7, 8}
    s.EAdd(e)
    s.LESet(e, "labelZ")
    s.HESet(e, "orange")
    res := s.EdgeFormat(e)
    assert.Contains(t, res, "label=")
    assert.Contains(t, res, "color=orange")
}

func TestEdgeFormatHiddenPublic(t *testing.T) {
    s := gvanim.NewStep()
    res := s.EdgeFormat([2]int{17, 28})
    assert.Contains(t, res, "style=invis")
}

func TestAnimationActionMethodsPublic(t *testing.T) {
    anim := gvanim.NewAnimation()
    anim.NextStep()
    anim.AddNode(101)
    anim.HighlightNode(201, "purple")
    anim.LabelNode(201, "Z")
    anim.UnlabelNode(201)
    anim.RemoveNode(201)
    anim.AddEdge(101, 301)
    anim.HighlightEdge(101, 301, "pink")
    anim.LabelEdge(101, 301, "F")
    anim.UnlabelEdge(101, 301)
    anim.RemoveEdge(101, 301)
    // No assertion, just check for panic/errors
}

func TestAnimationParseGoodPublic(t *testing.T) {
    anim := gvanim.NewAnimation()
    err := anim.Parse([]string{
        "an 17", "ae 17 18", "ln 17 labelB", "le 17 18 labelF",
        "hn 17", "he 17 18", "ns", "un 17", "ue 17 18", "rn 17", "re 17 18",
    })
    assert.NoError(t, err)
}

func TestAnimationParseBadPublic(t *testing.T) {
    anim := gvanim.NewAnimation()
    err := anim.Parse([]string{"badcmd 77"})
    assert.Error(t, err)
}

func TestAnimationParseBadFormatPublic(t *testing.T) {
    anim := gvanim.NewAnimation()
    err1 := anim.Parse([]string{"ae"})
    err2 := anim.Parse([]string{"an invalidnum"})
    assert.Error(t, err1)
    assert.Error(t, err2)
}