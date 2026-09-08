package at.markushi.ui.action;

import org.junit.Test;

import static org.junit.Assert.*;

public class DrawerActionTest {
    @Test
    public void testDrawerActionLineData() {
        DrawerAction drawerAction = new DrawerAction();
        assertNotNull(drawerAction.getLineData());
        assertEquals(12, drawerAction.getLineData().length);

        // check for correct center value
        assertEquals(0.5f, drawerAction.getLineData()[5], 0.00001);
    }
}