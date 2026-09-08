package com.example;

public class BootloaderSpoofer {
    private boolean spoofed;

    public BootloaderSpoofer() {
        this.spoofed = false;
    }

    public boolean isSpoofed() {
        return spoofed;
    }

    public void spoof() {
        if (!spoofed) {
            spoofed = true;
        }
    }

    public void reset() {
        spoofed = false;
    }

    public String status() {
        return spoofed ? "Spoofed" : "Not spoofed";
    }
}