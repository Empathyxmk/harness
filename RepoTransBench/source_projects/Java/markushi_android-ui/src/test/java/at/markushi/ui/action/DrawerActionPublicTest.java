package at.markushi.ui.action;

import org.junit.Test;

import static org.junit.Assert.*;

public class DrawerActionPublicTest {
    @Test
    public void testDrawerActionLineDataPublic() {
        DrawerAction drawerAction = new DrawerAction();
        assertNotNull(drawerAction.getLineData());
        assertEquals(12, drawerAction.getLineData().length);

        // check a value not checked in the original (index 7)
        assertTrue(drawerAction.getLineData()[7] >= 0f && drawerAction.getLineData()[7] <= 1f);

        // ensure at least one line does NOT have 0.5f value at a new index
        assertNotEquals(0.5f, drawerAction.getLineData()[2], 0.00001);
    }
}