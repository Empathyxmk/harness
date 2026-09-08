package adp.pathmorph;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class PlayToPauseMorphTest {

    @Test
    public void testInitialStateIsPlaying() {
        PlayToPauseMorph morph = new PlayToPauseMorph(true);
        assertTrue(morph.isPlaying());
        assertEquals("PLAY", morph.getState());
    }

    @Test
    public void testInitialStateIsPause() {
        PlayToPauseMorph morph = new PlayToPauseMorph(false);
        assertFalse(morph.isPlaying());
        assertEquals("PAUSE", morph.getState());
    }

    @Test
    public void testToggleFunctionality() {
        PlayToPauseMorph morph = new PlayToPauseMorph(true);
        morph.toggle();
        assertFalse(morph.isPlaying());
        assertEquals("PAUSE", morph.getState());
        morph.toggle();
        assertTrue(morph.isPlaying());
        assertEquals("PLAY", morph.getState());
    }
}