package adp.pathmorph;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class PlayToPauseMorphAdditionalTest {

    @Test
    public void testMultipleToggles() {
        PlayToPauseMorph morph = new PlayToPauseMorph(false);
        // Toggle 5 times, state should alternate each time
        boolean expected = false;
        for (int i = 0; i < 5; i++) {
            morph.toggle();
            expected = !expected;
            assertEquals(expected, morph.isPlaying());
        }
    }

    @Test
    public void testGetStateStrings() {
        PlayToPauseMorph morph = new PlayToPauseMorph(true);
        assertEquals("PLAY", morph.getState());
        morph.toggle();
        assertEquals("PAUSE", morph.getState());
    }

    @Test
    public void testEdgeCaseNoToggle() {
        PlayToPauseMorph morphPlay = new PlayToPauseMorph(true);
        assertEquals("PLAY", morphPlay.getState());
        PlayToPauseMorph morphPause = new PlayToPauseMorph(false);
        assertEquals("PAUSE", morphPause.getState());
    }

}