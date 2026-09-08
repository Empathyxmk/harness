package com.skydoves.preferenceroomdemo.entities;

import android.content.Context;
import androidx.test.core.app.ApplicationProvider;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class ProfileEntityPublicTest {

    private Profile publicProfile;

    @Before
    public void setup() {
        Context context = ApplicationProvider.getApplicationContext();
        // Use different values
        publicProfile = new Profile(context, "public_name", "public@email.org");
        publicProfile.setPhone("123987456"); // different phone
    }

    @Test
    public void testNamePublic() {
        assertEquals("public_name", publicProfile.getName());
    }

    @Test
    public void testEmailPublic() {
        assertEquals("public@email.org", publicProfile.getEmail());
    }

    @Test
    public void testPhonePublic() {
        assertEquals("123987456", publicProfile.getPhone());
    }
}