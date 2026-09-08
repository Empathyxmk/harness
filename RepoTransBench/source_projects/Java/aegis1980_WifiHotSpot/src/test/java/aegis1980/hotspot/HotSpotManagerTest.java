package aegis1980.hotspot;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class HotSpotManagerTest {

    @Test
    void testInitialState() {
        HotSpotManager manager = new HotSpotManager();
        assertFalse(manager.isEnabled());
        assertEquals("defaultSSID", manager.getSsid());
        assertEquals("password", manager.getPassword());
    }

    @Test
    void testEnableHotspotValid() {
        HotSpotManager manager = new HotSpotManager();
        boolean result = manager.enableHotspot("MySSID", "MyPass123");
        assertTrue(result);
        assertTrue(manager.isEnabled());
        assertEquals("MySSID", manager.getSsid());
        assertEquals("MyPass123", manager.getPassword());
    }

    @Test
    void testEnableHotspotInvalidSsid() {
        HotSpotManager manager = new HotSpotManager();
        assertFalse(manager.enableHotspot(null, "password123"));
        assertFalse(manager.enableHotspot("", "password123"));
        assertFalse(manager.isEnabled());
    }

    @Test
    void testEnableHotspotInvalidPassword() {
        HotSpotManager manager = new HotSpotManager();
        assertFalse(manager.enableHotspot("SSID", null));
        assertFalse(manager.enableHotspot("SSID", "short"));
        assertFalse(manager.isEnabled());
    }

    @Test
    void testDisableHotspot() {
        HotSpotManager manager = new HotSpotManager();
        manager.enableHotspot("SSID", "password123");
        assertTrue(manager.isEnabled());
        manager.disableHotspot();
        assertFalse(manager.isEnabled());
    }

    // NEW TESTS FOR FULL BRANCH COVERAGE

    @Test
    void testEnableHotspotPasswordExactly8() {
        HotSpotManager manager = new HotSpotManager();
        String password8 = "12345678"; // Exactly 8 chars
        boolean result = manager.enableHotspot("SSID2", password8);
        assertTrue(result);
        assertTrue(manager.isEnabled());
        assertEquals("SSID2", manager.getSsid());
        assertEquals(password8, manager.getPassword());
    }

    @Test
    void testDisablingTwice() {
        HotSpotManager manager = new HotSpotManager();
        // Disable even if not enabled, should not throw or change state
        manager.disableHotspot();
        assertFalse(manager.isEnabled());
        manager.enableHotspot("SSID", "password123");
        assertTrue(manager.isEnabled());
        manager.disableHotspot();
        assertFalse(manager.isEnabled());
        // Try disabling twice in a row
        manager.disableHotspot();
        assertFalse(manager.isEnabled());
    }

    @Test
    void testEnableHotspotPasswordWith8ButNullSSID() {
        HotSpotManager manager = new HotSpotManager();
        assertFalse(manager.enableHotspot(null, "12345678"));
        assertFalse(manager.isEnabled());
    }

    @Test
    void testEnableHotspotNullPassword() {
        HotSpotManager manager = new HotSpotManager();
        assertFalse(manager.enableHotspot("SSID", null));
        assertFalse(manager.isEnabled());
    }

    // Defensive: try changing SSID/password after hotspot enabled
    @Test
    void testMultipleEnables() {
        HotSpotManager manager = new HotSpotManager();
        assertTrue(manager.enableHotspot("SSID", "password123"));
        assertEquals("SSID", manager.getSsid());
        assertEquals("password123", manager.getPassword());
        assertTrue(manager.isEnabled());

        // Enable with new values
        assertTrue(manager.enableHotspot("SSID2", "password456"));
        assertEquals("SSID2", manager.getSsid());
        assertEquals("password456", manager.getPassword());
        assertTrue(manager.isEnabled());
    }

    // Blank password but valid SSID
    @Test
    void testEnableHotspotEmptyPassword() {
        HotSpotManager manager = new HotSpotManager();
        assertFalse(manager.enableHotspot("SSID", ""));
        assertFalse(manager.isEnabled());
    }
}