package public_tests

import (
	"fitchart"
)

// Type reexports so tests may use these identifiers as in Java public tests
type AnimationMode = fitchart.AnimationMode
const (
	LINEAR   = fitchart.LINEAR
	OVERDRAW = fitchart.OVERDRAW
)

type Renderer = fitchart.Renderer
type FitChartValue = fitchart.FitChartValue

type RectF = fitchart.RectF