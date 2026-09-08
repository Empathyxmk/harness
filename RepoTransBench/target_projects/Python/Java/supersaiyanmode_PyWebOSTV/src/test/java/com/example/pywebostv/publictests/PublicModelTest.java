package com.example.pywebostv.publictests;

import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class Device {
    private final Map<String, Object> data;
    Device(Map<String, Object> data) { this.data = data; }
    public Object getCapabilities() { return data.get("capabilities"); }
    public String getModelName() { return (String) data.get("modelName"); }
    public String getName() { return (String) data.get("friendlyName"); }
    public String getUuid() { return (String) data.get("udn"); }
}

class Application {
    private final Map<String, Object> data;
    Application(Map<String, Object> data) { this.data = data; }
    public String getId() { return (String) data.get("id"); }
    public String getTitle() { return (String) data.get("title"); }
    public String getIcon() { return (String) data.get("icon"); }
    public String toString() { return getTitle() + " " + getId(); }
}

public class PublicModelTest {

    @Test
    public void testDeviceModelPublic() {
        Map<String, Object> info = new HashMap<>();
        info.put("capabilities", Map.of("list", new String[]{"PublicCapability1", "PublicCapability2"}));
        info.put("modelName", "PublicLG123");
        info.put("friendlyName", "Public TV");
        info.put("udn", "Public-UUID");
        Device device = new Device(info);
        assertEquals(Map.of("list", new String[]{"PublicCapability1", "PublicCapability2"}), device.getCapabilities());
        assertEquals("PublicLG123", device.getModelName());
        assertEquals("Public TV", device.getName());
        assertEquals("Public-UUID", device.getUuid());
    }

    @Test
    public void testApplicationPublic() {
        Map<String, Object> data = new HashMap<>();
        data.put("id", "app.public");
        data.put("title", "Public App");
        data.put("icon", "publicicon.png");
        Application app = new Application(data);
        assertEquals("app.public", app.getId());
        assertEquals("Public App", app.getTitle());
        assertEquals("publicicon.png", app.getIcon());
        assertTrue(app.toString().contains("Public App"));
    }
}