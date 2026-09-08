package com.example;

public class KeepAwake {
    private boolean awake;

    public KeepAwake() {
        this.awake = false;
    }

    public boolean isAwake() {
        return awake;
    }

    public void activate() {
        if (!awake) {
            awake = true;
        }
    }

    public void deactivate() {
        if (awake) {
            awake = false;
        }
    }

    public void setAwake(boolean value) {
        if (value) {
            activate();
        } else {
            deactivate();
        }
    }

    public String getStatus() {
        if (awake) {
            return "Awake";
        } else {
            return "Sleeping";
        }
    }
}