package com.skydoves.preferenceroomdemo.components;

import android.content.Context;
import androidx.test.core.app.ApplicationProvider;
import com.skydoves.preferenceroomdemo.PreferenceRoomApplication;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class JunitComponentPublicTest {

    private JunitComponent publicJunitComponent;

    @Before
    public void setup() {
        Context context = ApplicationProvider.getApplicationContext();
        // Simulate creation with "other" data for public
        publicJunitComponent = new JunitComponent(context, "public_device_id");
    }

    @Test
    public void testDeviceIdIsSetPublic() {
        assertEquals("public_device_id", publicJunitComponent.getDeviceId());
    }

    @Test
    public void testDeviceIdIsNotDefaultPublic() {
        assertNotEquals("DEFAULT_DEVICE", publicJunitComponent.getDeviceId());
    }
}