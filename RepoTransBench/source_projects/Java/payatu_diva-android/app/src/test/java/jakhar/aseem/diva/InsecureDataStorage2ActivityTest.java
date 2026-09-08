package jakhar.aseem.diva;

import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.widget.EditText;

import org.junit.Before;
import org.junit.Test;
import org.robolectric.Robolectric;
import org.robolectric.android.controller.ActivityController;

import static org.junit.Assert.*;

public class InsecureDataStorage2ActivityTest {

    private InsecureDataStorage2Activity activity;

    @Before
    public void setUp() {
        ActivityController<InsecureDataStorage2Activity> controller = Robolectric.buildActivity(InsecureDataStorage2Activity.class).create().start();
        activity = controller.get();
    }

    @Test
    public void test_onCreate_createsDBAndTable() {
        // If DB/table creation fails, no exception should be raised.
    }

    @Test
    public void test_saveCredentials_insertsUserData() {
        EditText user = activity.findViewById(jakhar.aseem.diva.R.id.ids2Usr);
        EditText pass = activity.findViewById(jakhar.aseem.diva.R.id.ids2Pwd);
        user.setText("dbuser");
        pass.setText("dbpass");

        activity.saveCredentials(null);

        SQLiteDatabase db = activity.openOrCreateDatabase("ids2", activity.MODE_PRIVATE, null);
        Cursor cursor = db.rawQuery("SELECT user, password FROM myuser WHERE user='dbuser'", null);

        assertTrue(cursor.moveToFirst());
        assertEquals("dbuser", cursor.getString(0));
        assertEquals("dbpass", cursor.getString(1));
        cursor.close();
        db.close();
    }
}