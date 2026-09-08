package original

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "mapio_GraphvizAnim/gvanim"
    "mapio_GraphvizAnim/gvanim/action"
)

func TestAddNodeAction(t *testing.T) {
    s := []*gvanim.Step{gvanim.NewStep()}
    action.AddNode(42)(s)
    assert.Contains(t, s[len(s)-1].V(), 42)
}

func TestHighlightNodeAndLabelNode(t *testing.T) {
    s := []*gvanim.Step{gvanim.NewStep()}
    action.HighlightNode(2, "blue")(s)
    action.LabelNode(2, "lbl")(s)
    assert.Contains(t, s[len(s)-1].HV(), 2)
    assert.Contains(t, s[len(s)-1].LV(), 2)
}

func TestUnlabelAndRemoveNode(t *testing.T) {
    s := []*gvanim.Step{gvanim.NewStep()}
    action.AddNode(1)(s)
    action.LabelNode(1, "tok")(s)
    action.UnlabelNode(1)(s)
    assert.NotContains(t, s[len(s)-1].LV(), 1)
    action.RemoveNode(1)(s)
    assert.NotContains(t, s[len(s)-1].V(), 1)
}

func TestAddEdgeAndHighlightLabelUnlabelRemove(t *testing.T) {
    s := []*gvanim.Step{gvanim.NewStep()}
    action.AddNode(3)(s)
    action.AddNode(4)(s)
    action.AddEdge(3, 4)(s)
    action.HighlightEdge(3, 4, "green")(s)
    action.LabelEdge(3, 4, "X")(s)
    assert.Contains(t, s[len(s)-1].E(), [2]int{3, 4})
    assert.Contains(t, s[len(s)-1].HE(), [2]int{3, 4})
    assert.Contains(t, s[len(s)-1].LE(), [2]int{3, 4})
    action.UnlabelEdge(3, 4)(s)
    action.RemoveEdge(3, 4)(s)
    assert.NotContains(t, s[len(s)-1].E(), [2]int{3, 4})
}