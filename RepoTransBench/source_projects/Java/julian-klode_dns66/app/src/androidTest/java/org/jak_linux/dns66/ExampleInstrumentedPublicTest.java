package org.jak_linux.dns66;

import android.content.Context;
import androidx.test.platform.app.InstrumentationRegistry;
import androidx.test.ext.junit.runners.AndroidJUnit4;

import org.junit.Test;
import org.junit.runner.RunWith;

import static org.junit.Assert.*;

@RunWith(AndroidJUnit4.class)
public class ExampleInstrumentedPublicTest {
    @Test
    public void useAppContextPublic() throws Exception {
        // Use a different assert on the appContext, just check it's not null in public test
        Context appContext = InstrumentationRegistry.getTargetContext();

        assertNotNull(appContext);
    }
}