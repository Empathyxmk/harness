package at.markushi.ui.action;

import org.junit.Test;

import static org.junit.Assert.*;

public class PlusActionPublicTest {
    @Test
    public void testPlusActionLineDataPublic() {
        PlusAction plusAction = new PlusAction();
        assertNotNull(plusAction.getLineData());
        assertEquals(12, plusAction.getLineData().length);

        // check middle point of the vertical line (different index from original)
        assertNotEquals(0.5f, plusAction.getLineData()[1], 0.00001);

        // check another value in the array is within [0, 1]
        assertTrue(plusAction.getLineData()[3] >= 0f && plusAction.getLineData()[3] <= 1f);
    }
}