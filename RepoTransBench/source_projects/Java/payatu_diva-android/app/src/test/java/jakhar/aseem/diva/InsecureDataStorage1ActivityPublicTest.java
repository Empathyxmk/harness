package jakhar.aseem.diva;

import android.content.SharedPreferences;
import android.widget.EditText;

import org.junit.Before;
import org.junit.Test;
import org.robolectric.Robolectric;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.android.controller.ActivityController;

import static org.junit.Assert.*;

public class InsecureDataStorage1ActivityPublicTest {

    private InsecureDataStorage1Activity activity;

    @Before
    public void setUp() {
        ActivityController<InsecureDataStorage1Activity> controller = Robolectric.buildActivity(InsecureDataStorage1Activity.class).create().start();
        activity = controller.get();
    }

    @Test
    public void test_saveCredentials_savesToPrefs_public() {
        EditText user = activity.findViewById(jakhar.aseem.diva.R.id.ids1Usr);
        EditText pass = activity.findViewById(jakhar.aseem.diva.R.id.ids1Pwd);
        // Use new test values
        user.setText("publicuser");
        pass.setText("publicpass");

        activity.saveCredentials(null);

        SharedPreferences prefs = RuntimeEnvironment.application.getSharedPreferences("ids1", activity.MODE_PRIVATE);
        assertEquals("publicuser", prefs.getString("user", null));
        assertEquals("publicpass", prefs.getString("password", null));
    }
}