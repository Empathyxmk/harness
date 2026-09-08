package com.txusballesteros.widgets;

// Minimal fake classes to allow pure JVM tests to compile without Android full framework dependencies

public enum AnimationMode {
    LINEAR,
    OVERDRAW
}

public interface Renderer {
    android.graphics.Path buildPath(float animationProgress, float animationSeek);
}

public class FitChartValue {
    private float value;
    private int color;
    private float startAngle = 0;
    private float sweepAngle = 0;
    private android.graphics.Paint paint;

    public FitChartValue(float value, int color) { this.value = value; this.color = color; }
    public float getValue() { return value; }
    public int getColor() { return color; }

    public float getStartAngle() { return startAngle; }
    public float getSweepAngle() { return sweepAngle; }
    public void setStartAngle(float angle) { this.startAngle = angle; }
    public void setSweepAngle(float angle) { this.sweepAngle = angle; }
    public void setPaint(android.graphics.Paint paint) { this.paint = paint; }
    public android.graphics.Paint getPaint() { return paint; }
}