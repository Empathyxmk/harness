package jakhar.aseem.diva;

import android.webkit.WebView;
import android.widget.EditText;

import org.junit.Before;
import org.junit.Test;
import org.robolectric.Robolectric;
import org.robolectric.android.controller.ActivityController;

import static org.junit.Assert.*;

public class InputValidation2URISchemeActivityTest {

    private InputValidation2URISchemeActivity activity;

    @Before
    public void setUp() {
        ActivityController<InputValidation2URISchemeActivity> controller =
            Robolectric.buildActivity(InputValidation2URISchemeActivity.class).create().start();
        activity = controller.get();
    }

    @Test
    public void test_onCreate_setsLayoutAndJS() {
        WebView wview = activity.findViewById(jakhar.aseem.diva.R.id.ivi2wview);
        assertNotNull(wview);
        assertTrue(wview.getSettings().getJavaScriptEnabled());
    }

    @Test
    public void test_get_loadsUrlFromEditText() {
        EditText uri = activity.findViewById(jakhar.aseem.diva.R.id.ivi2uri);
        WebView wview = activity.findViewById(jakhar.aseem.diva.R.id.ivi2wview);

        uri.setText("https://payatu.com/");
        activity.get(null);

        assertEquals("https://payatu.com/", wview.getUrl());
    }
}