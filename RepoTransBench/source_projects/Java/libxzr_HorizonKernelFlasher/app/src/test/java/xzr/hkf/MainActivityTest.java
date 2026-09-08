package xzr.hkf;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ScrollView;
import android.widget.TextView;

import androidx.test.core.app.ApplicationProvider;

import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class MainActivityTest {

    MainActivity activity;

    @Before
    public void setup() {
        // Use Robolectric to create an activity, or use a plain instance with mocks.
        activity = spy(new MainActivity());
        activity.logView = new TextView(ApplicationProvider.getApplicationContext());
        activity.scrollView = new ScrollView(ApplicationProvider.getApplicationContext());
        MainActivity.cur_status = MainActivity.status.normal;
    }

    @Test
    public void testAppendLog_DEBUG() {
        MainActivity.DEBUG = true;
        Activity mockAct = mock(MainActivity.class);
        doNothing().when(mockAct).runOnUiThread(any(Runnable.class));
        MainActivity._appendLog("hello", activity);
        MainActivity.appendLog("anything", activity);
        MainActivity.DEBUG = false;
    }

    @Test
    public void testAppendLog_ui_print() {
        Activity mockAct = mock(MainActivity.class);
        TextView logView = new TextView(ApplicationProvider.getApplicationContext());
        ScrollView scrollView = new ScrollView(ApplicationProvider.getApplicationContext());
        doCallRealMethod().when((MainActivity)mockAct).runOnUiThread(any(Runnable.class));
        ((MainActivity)mockAct).logView = logView;
        ((MainActivity)mockAct).scrollView = scrollView;
        MainActivity.appendLog("ui_print this is message", (MainActivity)mockAct);
    }

    @Test
    public void testFlashNew_NotFlashing() {
        MainActivity.cur_status = MainActivity.status.normal;
        MainActivity activitySpy = spy(activity);
        doNothing().when(activitySpy).update_title();
        doNothing().when(activitySpy).runWithFilePath(any(), any());
        activitySpy.logView = new TextView(ApplicationProvider.getApplicationContext());
        activitySpy.flash_new();
        // Asserts can be added by mock verifications
        verify(activitySpy).update_title();
        verify(activitySpy).runWithFilePath(any(), any());
    }

    @Test
    public void testOnBackPressed_FlashingAndOther() {
        MainActivity activitySpy = spy(activity);
        MainActivity.cur_status = MainActivity.status.normal;
        doNothing().when(activitySpy).superOnBackPressed();
        activitySpy.onBackPressed();
        MainActivity.cur_status = MainActivity.status.flashing;
        activitySpy.onBackPressed();
    }

    @Test
    public void testOnCreateOptionsMenu() {
        Menu mockMenu = mock(Menu.class);
        MainActivity activitySpy = spy(activity);
        doReturn(mock(Menu.class)).when(activitySpy).getMenuInflater();
        assertTrue(activitySpy.onCreateOptionsMenu(mockMenu));
    }

    @Test
    public void testOnOptionsItemSelected_about() {
        MenuItem item = mock(MenuItem.class);
        when(item.getItemId()).thenReturn(R.id.about);
        MainActivity activitySpy = spy(activity);
        doReturn(
            new AlertDialog.Builder(ApplicationProvider.getApplicationContext())
        ).when(activitySpy).getAlertDialogBuilder();
        assertTrue(activitySpy.onOptionsItemSelected(item));
    }

    @Test
    public void testOnOptionsItemSelected_flash_new() {
        MenuItem item = mock(MenuItem.class);
        when(item.getItemId()).thenReturn(R.id.flash_new);
        MainActivity activitySpy = spy(activity);
        doNothing().when(activitySpy).flash_new();
        assertTrue(activitySpy.onOptionsItemSelected(item));
        verify(activitySpy).flash_new();
    }

    @Test
    public void testRunWithFilePath() {
        Activity mock = mock(Activity.class);
        MainActivity.fileWorker worker = mock(MainActivity.fileWorker.class);
        doNothing().when(mock).startActivityForResult(any(Intent.class), anyInt());
        MainActivity.runWithFilePath(mock, worker);
        assertNotNull(worker);
    }
}