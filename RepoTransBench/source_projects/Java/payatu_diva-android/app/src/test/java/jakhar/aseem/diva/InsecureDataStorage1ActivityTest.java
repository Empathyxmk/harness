package jakhar.aseem.diva;

import android.content.SharedPreferences;
import android.preference.PreferenceManager;
import android.widget.EditText;

import org.junit.Before;
import org.junit.Test;
import org.robolectric.Robolectric;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.android.controller.ActivityController;

import static org.junit.Assert.*;

public class InsecureDataStorage1ActivityTest {

    private InsecureDataStorage1Activity activity;

    @Before
    public void setUp() {
        ActivityController<InsecureDataStorage1Activity> controller = Robolectric.buildActivity(InsecureDataStorage1Activity.class).create().start();
        activity = controller.get();
    }

    @Test
    public void test_onCreate_setsLayout() {
        // Should set layout without exception
    }

    @Test
    public void test_saveCredentials_storesCredentials() {
        EditText user = activity.findViewById(jakhar.aseem.diva.R.id.ids1Usr);
        EditText pass = activity.findViewById(jakhar.aseem.diva.R.id.ids1Pwd);
        user.setText("testuser");
        pass.setText("secret");

        activity.saveCredentials(null);

        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(activity);
        assertEquals("testuser", prefs.getString("user", ""));
        assertEquals("secret", prefs.getString("password", ""));
    }
}