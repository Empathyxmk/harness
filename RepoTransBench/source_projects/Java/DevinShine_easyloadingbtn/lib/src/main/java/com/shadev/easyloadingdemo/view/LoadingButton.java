// ... rest of the code ...
// Add at the end of the class (before the closing brace)
    // Helper methods for testability
    public int getTargetProgress() { return this.targetProgress; }
    public boolean isCompleted() { return this.isCompleted; }
    public boolean isShowArc() { return this.isShowArc; }
    public void setShowArc(boolean showArc) { this.isShowArc = showArc; }
    public void setCompleted(boolean completed) { this.isCompleted = completed; }
    public void performCompleteCallback() {
        if(this.callback != null) callback.complete();
    }
    // Allow test override resource loads
    protected Drawable getDrawable(int id) {
        return getResources().getDrawable(id);
    }
    public void setCallback(Callback callback) {
        this.callback = callback;
    }