package com.skydoves.preferenceroomdemo.components;

import android.content.Context;
import androidx.test.core.app.ApplicationProvider;
import com.skydoves.preferenceroomdemo.PreferenceRoomApplication;
import com.skydoves.preferenceroomdemo.entities.Profile;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class AppComponentPublicTest {
    private Profile publicProfile;

    @Before
    public void setup() {
        Context context = ApplicationProvider.getApplicationContext();
        // Use a "public" suffix for preference simulation, or mock distinct data
        publicProfile = new Profile(context, "public_test_user", "public@email.com");
    }

    @Test
    public void testProfileNameIsSetPublic() {
        // Use different data for the public test
        assertEquals("public_test_user", publicProfile.getName());
    }

    @Test
    public void testProfileEmailIsSetPublic() {
        assertEquals("public@email.com", publicProfile.getEmail());
    }
}