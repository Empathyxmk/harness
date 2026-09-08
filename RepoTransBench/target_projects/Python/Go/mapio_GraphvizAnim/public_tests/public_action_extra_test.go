package public_tests

import (
    "testing"
    "github.com/stretchr/testify/assert"
    "mapio_GraphvizAnim/gvanim"
    "mapio_GraphvizAnim/gvanim/action"
)

func TestAddNodeActionPublic(t *testing.T) {
    s := []*gvanim.Step{gvanim.NewStep()}
    action.AddNode(12)(s)
    assert.Contains(t, s[len(s)-1].V(), 12)
}

func TestHighlightNodeAndLabelNodePublic(t *testing.T) {
    s := []*gvanim.Step{gvanim.NewStep()}
    action.HighlightNode(20, "red")(s)
    action.LabelNode(20, "lbl2")(s)
    assert.Contains(t, s[len(s)-1].HV(), 20)
    assert.Contains(t, s[len(s)-1].LV(), 20)
}

func TestUnlabelAndRemoveNodePublic(t *testing.T) {
    s := []*gvanim.Step{gvanim.NewStep()}
    action.AddNode(9)(s)
    action.LabelNode(9, "zzz")(s)
    action.UnlabelNode(9)(s)
    assert.NotContains(t, s[len(s)-1].LV(), 9)
    action.RemoveNode(9)(s)
    assert.NotContains(t, s[len(s)-1].V(), 9)
}

func TestAddEdgeAndHighlightLabelUnlabelRemovePublic(t *testing.T) {
    s := []*gvanim.Step{gvanim.NewStep()}
    action.AddNode(6)(s)
    action.AddNode(13)(s)
    action.AddEdge(6, 13)(s)
    action.HighlightEdge(6, 13, "purple")(s)
    action.LabelEdge(6, 13, "Y")(s)
    assert.Contains(t, s[len(s)-1].E(), [2]int{6, 13})
    assert.Contains(t, s[len(s)-1].HE(), [2]int{6, 13})
    assert.Contains(t, s[len(s)-1].LE(), [2]int{6, 13})
    action.UnlabelEdge(6, 13)(s)
    action.RemoveEdge(6, 13)(s)
    assert.NotContains(t, s[len(s)-1].E(), [2]int{6, 13})
}