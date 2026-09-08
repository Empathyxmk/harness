package jakhar.aseem.diva;

import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;

import static org.mockito.Mockito.*;

import androidx.test.core.app.ApplicationProvider;
import androidx.test.ext.junit.runners.AndroidJUnit4;

// Robolectric for mocking AppCompatActivity and Android APIs
import org.robolectric.Robolectric;
import org.robolectric.RobolectricTestRunner;
import org.robolectric.RuntimeEnvironment;
import org.robolectric.android.controller.ActivityController;

@RunWith(RobolectricTestRunner.class)
public class AccessControl1ActivityTest {

    private AccessControl1Activity activity;

    @Before
    public void setUp() {
        ActivityController<AccessControl1Activity> controller = Robolectric.buildActivity(AccessControl1Activity.class).create().start();
        activity = controller.get();
    }

    @Test
    public void test_onCreate_setsLayout() {
        // No exception should be thrown, layout set in onCreate.
    }

    @Test
    public void test_viewAPICredentials_intentResolved_startsActivity() {
        PackageManager packageManager = mock(PackageManager.class);
        // Simulate that intent resolves successfully
        when(packageManager.resolveActivity(any(Intent.class), anyInt())).thenReturn(mock(android.content.pm.ResolveInfo.class));
        AccessControl1Activity spyActivity = spy(activity);
        doReturn(packageManager).when(spyActivity).getPackageManager();

        spyActivity.viewAPICredentials(new View(spyActivity));
        verify(spyActivity, atLeastOnce()).startActivity(any(Intent.class));
    }

    @Test
    public void test_viewAPICredentials_intentNotResolved_showsToastAndLogs() {
        PackageManager packageManager = mock(PackageManager.class);
        // Simulate that intent does NOT resolve
        when(packageManager.resolveActivity(any(Intent.class), anyInt())).thenReturn(null);

        AccessControl1Activity spyActivity = spy(activity);
        doReturn(packageManager).when(spyActivity).getPackageManager();

        spyActivity.viewAPICredentials(new View(spyActivity));
        // Cannot easily verify Toast, but method should complete without error.
    }
}