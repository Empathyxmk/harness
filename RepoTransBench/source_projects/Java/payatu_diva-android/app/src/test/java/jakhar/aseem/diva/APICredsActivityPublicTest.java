package jakhar.aseem.diva;

import android.os.Bundle;
import android.widget.TextView;

import org.junit.Before;
import org.junit.Test;
import org.robolectric.Robolectric;
import org.robolectric.android.controller.ActivityController;

import static org.junit.Assert.*;

public class APICredsActivityPublicTest {
    private APICredsActivity activity;

    @Before
    public void setUp() {
        ActivityController<APICredsActivity> controller = Robolectric.buildActivity(APICredsActivity.class).create().start();
        activity = controller.get();
    }

    @Test
    public void test_onCreate_setsAPIText_public() {
        TextView tv = activity.findViewById(jakhar.aseem.diva.R.id.apicTextView);
        assertNotNull(tv);
        // Public: Different API Key/Username/Password for testing text difference
        String notExpected = "API Key: 123secretapikey123\nAPI User name: diva\nAPI Password: p@ssword";
        String actual = tv.getText().toString();
        assertNotEquals(notExpected, actual);

        // Partial check: Check for presence of "API Key:" and ":" format
        assertTrue(actual.contains("API Key:"));
        assertTrue(actual.contains("API User name:"));
        assertTrue(actual.contains("API Password:"));
        // The API Key should not be "123secretapikey123"
        assertFalse(actual.contains("123secretapikey123"));
    }
}