package aegis1980.hotspot;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class HotSpotManagerPublicTest {

    @Test
    void testInitialStatePublic() {
        HotSpotManager manager = new HotSpotManager();
        assertFalse(manager.isEnabled());
        assertEquals("defaultSSID", manager.getSsid());
        assertEquals("password", manager.getPassword());
    }

    @Test
    void testEnableHotspotValidPublic() {
        HotSpotManager manager = new HotSpotManager();
        boolean result = manager.enableHotspot("PublicSSID", "Another123");
        assertTrue(result);
        assertTrue(manager.isEnabled());
        assertEquals("PublicSSID", manager.getSsid());
        assertEquals("Another123", manager.getPassword());
    }

    @Test
    void testEnableHotspotInvalidSsidPublic() {
        HotSpotManager manager = new HotSpotManager();
        assertFalse(manager.enableHotspot(null, "publicpass"));
        assertFalse(manager.enableHotspot("", "publicpass"));
        assertFalse(manager.isEnabled());
    }

    @Test
    void testEnableHotspotInvalidPasswordPublic() {
        HotSpotManager manager = new HotSpotManager();
        assertFalse(manager.enableHotspot("MyNetwork", null));
        assertFalse(manager.enableHotspot("MyNetwork", "short1"));
        assertFalse(manager.isEnabled());
    }

    @Test
    void testDisableHotspotPublic() {
        HotSpotManager manager = new HotSpotManager();
        manager.enableHotspot("Network42", "SuperPass9");
        assertTrue(manager.isEnabled());
        manager.disableHotspot();
        assertFalse(manager.isEnabled());
    }

    @Test
    void testEnableHotspotPasswordExactly8Public() {
        HotSpotManager manager = new HotSpotManager();
        String password8 = "abcdefgh"; // Exactly 8 chars, different from original test
        boolean result = manager.enableHotspot("SSID_Public", password8);
        assertTrue(result);
        assertTrue(manager.isEnabled());
        assertEquals("SSID_Public", manager.getSsid());
        assertEquals(password8, manager.getPassword());
    }

    @Test
    void testDisablingTwicePublic() {
        HotSpotManager manager = new HotSpotManager();
        manager.disableHotspot();
        assertFalse(manager.isEnabled());
        manager.enableHotspot("PublicSSID2", "ExtraPass2");
        assertTrue(manager.isEnabled());
        manager.disableHotspot();
        assertFalse(manager.isEnabled());
        manager.disableHotspot();
        assertFalse(manager.isEnabled());
    }

    @Test
    void testEnableHotspotPasswordWith8ButNullSSIDPublic() {
        HotSpotManager manager = new HotSpotManager();
        assertFalse(manager.enableHotspot(null, "abcdefgh"));
        assertFalse(manager.isEnabled());
    }

    @Test
    void testEnableHotspotNullPasswordPublic() {
        HotSpotManager manager = new HotSpotManager();
        assertFalse(manager.enableHotspot("AnotherNet", null));
        assertFalse(manager.isEnabled());
    }

    @Test
    void testMultipleEnablesPublic() {
        HotSpotManager manager = new HotSpotManager();
        assertTrue(manager.enableHotspot("FirstSSID", "initPass99"));
        assertEquals("FirstSSID", manager.getSsid());
        assertEquals("initPass99", manager.getPassword());
        assertTrue(manager.isEnabled());

        assertTrue(manager.enableHotspot("SecondSSID", "reNewPass0"));
        assertEquals("SecondSSID", manager.getSsid());
        assertEquals("reNewPass0", manager.getPassword());
        assertTrue(manager.isEnabled());
    }

    @Test
    void testEnableHotspotEmptyPasswordPublic() {
        HotSpotManager manager = new HotSpotManager();
        assertFalse(manager.enableHotspot("MyNet", ""));
        assertFalse(manager.isEnabled());
    }
}