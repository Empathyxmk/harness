package adp.pathmorph;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class PlayToPauseMorphPublicTest {

    @Test
    public void testInitialStateIsPausePublic() {
        PlayToPauseMorph morph = new PlayToPauseMorph(false);
        assertFalse(morph.isPlaying());
        assertEquals("PAUSE", morph.getState());
    }

    @Test
    public void testInitialStateIsPlayingPublic() {
        PlayToPauseMorph morph = new PlayToPauseMorph(true);
        assertTrue(morph.isPlaying());
        assertEquals("PLAY", morph.getState());
    }

    @Test
    public void testDoubleToggleFunctionalityPublic() {
        PlayToPauseMorph morph = new PlayToPauseMorph(false);
        morph.toggle();
        assertTrue(morph.isPlaying());
        assertEquals("PLAY", morph.getState());
        morph.toggle();
        assertFalse(morph.isPlaying());
        assertEquals("PAUSE", morph.getState());
    }
}