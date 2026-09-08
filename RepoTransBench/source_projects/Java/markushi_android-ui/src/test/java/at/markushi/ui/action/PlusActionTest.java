package at.markushi.ui.action;

import org.junit.Test;

import static org.junit.Assert.*;

public class PlusActionTest {
    @Test
    public void testPlusActionLineData() {
        PlusAction plusAction = new PlusAction();
        assertNotNull(plusAction.getLineData());
        assertEquals(12, plusAction.getLineData().length);

        // check main vertical line
        assertEquals(0.5f, plusAction.getLineData()[0], 0.00001);
        // check main horizontal line
        assertEquals(0.5f, plusAction.getLineData()[5], 0.00001);
    }
}