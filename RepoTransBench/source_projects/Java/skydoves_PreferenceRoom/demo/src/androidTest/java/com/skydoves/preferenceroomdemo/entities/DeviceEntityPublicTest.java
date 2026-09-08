package com.skydoves.preferenceroomdemo.entities;

import android.content.Context;
import androidx.test.core.app.ApplicationProvider;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class DeviceEntityPublicTest {

    private Device publicDevice;

    @Before
    public void setup() {
        Context context = ApplicationProvider.getApplicationContext();
        // Use different device name and type
        publicDevice = new Device(context, "public_device_alpha", "public_type_beta");
        publicDevice.setMacAddress("AA:BB:CC:DD:EE:FF");
    }

    @Test
    public void testDeviceNamePublic() {
        assertEquals("public_device_alpha", publicDevice.getDeviceName());
    }

    @Test
    public void testDeviceTypePublic() {
        assertEquals("public_type_beta", publicDevice.getDeviceType());
    }

    @Test
    public void testMacAddressPublic() {
        assertEquals("AA:BB:CC:DD:EE:FF", publicDevice.getMacAddress());
    }
}