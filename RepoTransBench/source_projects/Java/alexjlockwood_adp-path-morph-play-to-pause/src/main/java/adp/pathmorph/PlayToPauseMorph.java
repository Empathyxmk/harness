package adp.pathmorph;

public class PlayToPauseMorph {
    private boolean isPlaying;

    public PlayToPauseMorph(boolean initialState) {
        this.isPlaying = initialState;
    }

    public boolean isPlaying() {
        return isPlaying;
    }

    public void toggle() {
        isPlaying = !isPlaying;
    }

    public String getState() {
        return isPlaying ? "PLAY" : "PAUSE";
    }
}