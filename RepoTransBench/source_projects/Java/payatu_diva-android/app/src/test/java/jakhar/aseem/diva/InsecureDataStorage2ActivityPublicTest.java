package jakhar.aseem.diva;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.widget.EditText;

import org.junit.Before;
import org.junit.Test;
import org.robolectric.Robolectric;
import org.robolectric.android.controller.ActivityController;

import static org.junit.Assert.*;

public class InsecureDataStorage2ActivityPublicTest {

    private InsecureDataStorage2Activity activity;

    @Before
    public void setUp() {
        ActivityController<InsecureDataStorage2Activity> controller = Robolectric.buildActivity(InsecureDataStorage2Activity.class).create().start();
        activity = controller.get();
    }

    @Test
    public void test_onCreate_createsDBAndTable_public() {
        // DB/table creation should succeed
        SQLiteDatabase db = activity.openOrCreateDatabase("ids2", activity.MODE_PRIVATE, null);
        Cursor cursor = db.rawQuery("SELECT name FROM sqlite_master WHERE type='table' AND name='myuser'", null);
        assertTrue(cursor.moveToFirst());
        cursor.close();
        db.close();
    }

    @Test
    public void test_saveCredentials_insertsUserData_public() {
        EditText user = activity.findViewById(jakhar.aseem.diva.R.id.ids2Usr);
        EditText pass = activity.findViewById(jakhar.aseem.diva.R.id.ids2Pwd);
        // Change user/pass values from the original test
        user.setText("anotheruser");
        pass.setText("anotherpass");

        activity.saveCredentials(null);

        SQLiteDatabase db = activity.openOrCreateDatabase("ids2", activity.MODE_PRIVATE, null);
        Cursor cursor = db.rawQuery("SELECT user, password FROM myuser WHERE user='anotheruser'", null);

        assertTrue(cursor.moveToFirst());
        assertEquals("anotheruser", cursor.getString(0));
        assertEquals("anotherpass", cursor.getString(1));
        cursor.close();
        db.close();
    }
}