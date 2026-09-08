package adp.pathmorph;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class PlayToPauseMorphAdditionalPublicTest {

    @Test
    public void testMultipleTogglesPublic() {
        PlayToPauseMorph morph = new PlayToPauseMorph(true);
        // Toggle 4 times, state should alternate each time
        boolean expected = true;
        for (int i = 0; i < 4; i++) {
            morph.toggle();
            expected = !expected;
            assertEquals(expected, morph.isPlaying());
        }
    }

    @Test
    public void testGetStateStringsPublic() {
        PlayToPauseMorph morph = new PlayToPauseMorph(false);
        assertEquals("PAUSE", morph.getState());
        morph.toggle();
        assertEquals("PLAY", morph.getState());
    }

    @Test
    public void testEdgeCaseNoTogglePublic() {
        PlayToPauseMorph morphPause = new PlayToPauseMorph(false);
        assertEquals("PAUSE", morphPause.getState());
        PlayToPauseMorph morphPlay = new PlayToPauseMorph(true);
        assertEquals("PLAY", morphPlay.getState());
    }
}