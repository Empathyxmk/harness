package jakhar.aseem.diva;

import android.os.Bundle;
import android.widget.TextView;

import org.junit.Before;
import org.junit.Test;
import org.robolectric.Robolectric;
import org.robolectric.android.controller.ActivityController;

import static org.junit.Assert.*;

public class APICredsActivityTest {
    private APICredsActivity activity;

    @Before
    public void setUp() {
        ActivityController<APICredsActivity> controller = Robolectric.buildActivity(APICredsActivity.class).create().start();
        activity = controller.get();
    }

    @Test
    public void test_onCreate_setsAPIText() {
        TextView tv = activity.findViewById(jakhar.aseem.diva.R.id.apicTextView);
        assertNotNull(tv);
        String expected = "API Key: 123secretapikey123\nAPI User name: diva\nAPI Password: p@ssword";
        assertEquals(expected, tv.getText().toString());
    }
}