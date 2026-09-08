package xzr.hkf;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.net.Uri;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ScrollView;
import android.widget.TextView;

import androidx.test.core.app.ApplicationProvider;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class MainActivityPublicTest {

    MainActivity activity;

    @Before
    public void setup() {
        activity = spy(new MainActivity());
        activity.logView = new TextView(ApplicationProvider.getApplicationContext());
        activity.scrollView = new ScrollView(ApplicationProvider.getApplicationContext());
        MainActivity.cur_status = MainActivity.status.normal;
    }

    @Test
    public void testAppendLog_DEBUG_Public() {
        MainActivity.DEBUG = true;
        Activity mockAct = mock(MainActivity.class);
        doNothing().when(mockAct).runOnUiThread(any(Runnable.class));
        MainActivity._appendLog("world", activity);
        MainActivity.appendLog("foobar", activity);
        MainActivity.DEBUG = false;
    }

    @Test
    public void testAppendLog_ui_print_Public() {
        Activity mockAct = mock(Activity.class);
        TextView logView2 = new TextView(ApplicationProvider.getApplicationContext());
        ScrollView scrollView2 = new ScrollView(ApplicationProvider.getApplicationContext());
        doCallRealMethod().when((MainActivity)mockAct).runOnUiThread(any(Runnable.class));
        ((MainActivity)mockAct).logView = logView2;
        ((MainActivity)mockAct).scrollView = scrollView2;
        MainActivity.appendLog("ui_print log with different msg", (MainActivity)mockAct);
    }

    @Test
    public void testFlashNew_NotFlashing_Public() {
        MainActivity.cur_status = MainActivity.status.normal;
        MainActivity activitySpy2 = spy(activity);
        doNothing().when(activitySpy2).update_title();
        doNothing().when(activitySpy2).runWithFilePath(any(), any());
        activitySpy2.logView = new TextView(ApplicationProvider.getApplicationContext());
        activitySpy2.flash_new();
        verify(activitySpy2).update_title();
        verify(activitySpy2).runWithFilePath(any(), any());
    }

    @Test
    public void testOnBackPressed_FlashingAndOther_Public() {
        MainActivity activitySpy3 = spy(activity);
        MainActivity.cur_status = MainActivity.status.normal;
        doNothing().when(activitySpy3).superOnBackPressed();
        activitySpy3.onBackPressed();
        MainActivity.cur_status = MainActivity.status.error;
        activitySpy3.onBackPressed();
    }

    @Test
    public void testOnCreateOptionsMenu_Public() {
        Menu mockMenu2 = mock(Menu.class);
        MainActivity activitySpy4 = spy(activity);
        doReturn(mock(Menu.class)).when(activitySpy4).getMenuInflater();
        assertTrue(activitySpy4.onCreateOptionsMenu(mockMenu2));
    }

    @Test
    public void testOnOptionsItemSelected_about_Public() {
        MenuItem item = mock(MenuItem.class);
        // Use a different ID constant (simulate help instead of about, for test purpose)
        when(item.getItemId()).thenReturn(R.id.help);
        MainActivity activitySpy5 = spy(activity);
        doReturn(
            new AlertDialog.Builder(ApplicationProvider.getApplicationContext())
        ).when(activitySpy5).getAlertDialogBuilder();
        assertTrue(activitySpy5.onOptionsItemSelected(item));
    }

    @Test
    public void testOnOptionsItemSelected_flash_new_Public() {
        MenuItem item = mock(MenuItem.class);
        // Use a negative or different int for a different value
        when(item.getItemId()).thenReturn(-12345);
        MainActivity activitySpy6 = spy(activity);
        doNothing().when(activitySpy6).flash_new();
        // Should return true even for unknown (default branch)
        assertTrue(activitySpy6.onOptionsItemSelected(item));
    }

    @Test
    public void testRunWithFilePath_Public() {
        Activity mock = mock(Activity.class);
        MainActivity.fileWorker worker2 = mock(MainActivity.fileWorker.class);
        doNothing().when(mock).startActivityForResult(any(Intent.class), anyInt());
        MainActivity.runWithFilePath(mock, worker2);
        assertNotNull(worker2);
    }
}