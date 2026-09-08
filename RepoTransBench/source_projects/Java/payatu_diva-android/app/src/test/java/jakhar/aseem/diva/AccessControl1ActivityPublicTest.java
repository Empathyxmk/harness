package jakhar.aseem.diva;

import org.junit.Test;
import org.robolectric.Robolectric;
import org.robolectric.android.controller.ActivityController;

import static org.junit.Assert.*;

public class AccessControl1ActivityPublicTest {
    @Test
    public void test_activity_starts_and_layout_public() {
        ActivityController<AccessControl1Activity> controller = Robolectric.buildActivity(AccessControl1Activity.class);
        AccessControl1Activity activity = controller.create().start().get();
        assertNotNull(activity.findViewById(jakhar.aseem.diva.R.id.ac1ViewCredsBtn));
    }
}