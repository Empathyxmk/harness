package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import com.picklepete.pyicloud.services.PyiCloudServiceMock;
import java.util.Map;

public class FindMyiPhoneServiceTest {

    private PyiCloudServiceMock service;

    @BeforeEach
    public void setUp() {
        service = new PyiCloudServiceMock(
            PyiCloudServiceMock.AUTHENTICATED_USER,
            PyiCloudServiceMock.VALID_PASSWORD
        );
    }

    @Test
    public void testDevices() {
        // Mock service.devices returns a list of device objects
        Iterable<Map<String, Object>> devices = service.getDevices();
        int count = 0;
        for (Map<String, Object> device : devices) {
            // Each field should be present/not null as in Python tests
            assertNotNull(device.get("canWipeAfterLock"));
            assertNotNull(device.get("baUUID"));
            assertNotNull(device.get("wipeInProgress"));
            assertNotNull(device.get("lostModeEnabled"));
            assertNotNull(device.get("activationLocked"));
            assertNotNull(device.get("passcodeLength"));
            assertNotNull(device.get("deviceStatus"));
            assertNotNull(device.get("features"));
            assertNotNull(device.get("lowPowerMode"));
            assertNotNull(device.get("rawDeviceModel"));
            assertNotNull(device.get("id"));
            assertNotNull(device.get("isLocating"));
            assertNotNull(device.get("modelDisplayName"));
            assertNotNull(device.get("lostTimestamp"));
            assertNotNull(device.get("batteryLevel"));
            assertNotNull(device.get("locationEnabled"));
            assertNotNull(device.get("locFoundEnabled"));
            assertNotNull(device.get("fmlyShare"));
            assertNotNull(device.get("lostModeCapable"));
            assertNull(device.get("wipedTimestamp"));
            assertNotNull(device.get("deviceDisplayName"));
            assertNotNull(device.get("audioChannels"));
            assertNotNull(device.get("locationCapable"));
            assertNotNull(device.get("batteryStatus"));
            assertNull(device.get("trackingInfo"));
            assertNotNull(device.get("name"));
            assertNotNull(device.get("isMac"));
            assertNotNull(device.get("thisDevice"));
            assertNotNull(device.get("deviceClass"));
            assertNotNull(device.get("deviceModel"));
            assertNotNull(device.get("maxMsgChar"));
            assertNotNull(device.get("darkWake"));
            assertNull(device.get("remoteWipe"));

            // Nested .data version
            Map<String, Object> data = (Map<String, Object>)device.get("data");
            assertNotNull(data.get("canWipeAfterLock"));
            assertNotNull(data.get("baUUID"));
            assertNotNull(data.get("wipeInProgress"));
            assertNotNull(data.get("lostModeEnabled"));
            assertNotNull(data.get("activationLocked"));
            assertNotNull(data.get("passcodeLength"));
            assertNotNull(data.get("deviceStatus"));
            assertNotNull(data.get("features"));
            assertNotNull(data.get("lowPowerMode"));
            assertNotNull(data.get("rawDeviceModel"));
            assertNotNull(data.get("id"));
            assertNotNull(data.get("isLocating"));
            assertNotNull(data.get("modelDisplayName"));
            assertNotNull(data.get("lostTimestamp"));
            assertNotNull(data.get("batteryLevel"));
            assertNotNull(data.get("locationEnabled"));
            assertNotNull(data.get("locFoundEnabled"));
            assertNotNull(data.get("fmlyShare"));
            assertNotNull(data.get("lostModeCapable"));
            assertNull(data.get("wipedTimestamp"));
            assertNotNull(data.get("deviceDisplayName"));
            assertNotNull(data.get("audioChannels"));
            assertNotNull(data.get("locationCapable"));
            assertNotNull(data.get("batteryStatus"));
            assertNull(data.get("trackingInfo"));
            assertNotNull(data.get("name"));
            assertNotNull(data.get("isMac"));
            assertNotNull(data.get("thisDevice"));
            assertNotNull(data.get("deviceClass"));
            assertNotNull(data.get("deviceModel"));
            assertNotNull(data.get("maxMsgChar"));
            assertNotNull(data.get("darkWake"));
            assertNull(data.get("remoteWipe"));
            count++;
        }
        assertEquals(13, count);
    }
}