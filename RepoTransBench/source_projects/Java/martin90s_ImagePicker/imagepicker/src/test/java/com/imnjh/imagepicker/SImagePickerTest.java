package com.imnjh.imagepicker;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.support.v4.app.Fragment;

import com.imnjh.imagepicker.activity.PhotoPickerActivity;

import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;

import static org.junit.Assert.*;

public class SImagePickerTest {

    static class DummyConfig extends PickerConfig {
        private Context ctx;
        DummyConfig(Context ctx) { this.ctx = ctx; }
        @Override public Context getAppContext() { return ctx; }
    }

    static class DummyActivity extends Activity {
        public Intent lastIntent;
        public int lastRequestCode;
        @Override
        public void startActivityForResult(Intent intent, int requestCode) {
            lastIntent = intent;
            lastRequestCode = requestCode;
        }
    }

    static class DummyFragment extends Fragment {
        private Activity act;
        public Intent lastIntent;
        public int lastRequestCode;

        DummyFragment(Activity act) { this.act = act; }
        @Override
        public Activity getActivity() { return act; }
        @Override
        public Context getContext() { return act; }
        @Override
        public void startActivityForResult(Intent intent, int requestCode) {
            lastIntent = intent;
            lastRequestCode = requestCode;
        }
    }

    DummyActivity dummyActivity;
    DummyFragment dummyFragment;
    @Before
    public void setUp() {
        dummyActivity = new DummyActivity();
        dummyFragment = new DummyFragment(dummyActivity);
        SImagePicker.init(new DummyConfig(dummyActivity));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testGetPickerConfig_exceptionIfNotInitialized() {
        SImagePicker picker = SImagePicker.from(dummyActivity);
        // Unset for testing
        java.lang.reflect.Field field;
        try {
            field = SImagePicker.class.getDeclaredField("pickerConfig");
            field.setAccessible(true);
            field.set(null, null);
        } catch (Exception e) { throw new RuntimeException(e); }
        SImagePicker.getPickerConfig();
    }

    @Test(expected = IllegalArgumentException.class)
    public void testForResult_noInit_throws() {
        java.lang.reflect.Field field;
        try {
            field = SImagePicker.class.getDeclaredField("pickerConfig");
            field.setAccessible(true);
            field.set(null, null);
        } catch (Exception e) { throw new RuntimeException(e); }
        SImagePicker picker = SImagePicker.from(dummyActivity);
        picker.forResult(1);
    }

    @Test
    public void testFromActivityAndFromFragment() {
        SImagePicker picker1 = SImagePicker.from(dummyActivity);
        assertNotNull(picker1);
        SImagePicker picker2 = SImagePicker.from(dummyFragment);
        assertNotNull(picker2);
    }

    @Test
    public void testMaxCountRowCountPickModeCropFileShowCameraPickTextSetSelected() {
        SImagePicker picker = SImagePicker.from(dummyActivity);
        ArrayList<String> selected = new ArrayList<>();
        picker.maxCount(5).rowCount(2).pickMode(SImagePicker.MODE_AVATAR)
                .cropFilePath("test.jpg").showCamera(true).pickText(123)
                .setSelected(selected);
        // method chain should work, no exceptions
    }

    @Test
    public void testForResultCallsActivityAndFragment() {
        SImagePicker pickerA = SImagePicker.from(dummyActivity);
        pickerA.forResult(99);
        assertNotNull(dummyActivity.lastIntent);
        assertEquals(99, dummyActivity.lastRequestCode);

        SImagePicker pickerF = SImagePicker.from(dummyFragment);
        pickerF.forResult(66);
        assertNotNull(dummyFragment.lastIntent);
        assertEquals(66, dummyFragment.lastRequestCode);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testForResult_neitherActivityNorFragment() {
        SImagePicker picker = new SImagePicker(null) {
            // No activity, no fragment
        };
        java.lang.reflect.Field f;
        try {
            f = SImagePicker.class.getDeclaredField("pickerConfig");
            f.setAccessible(true);
            f.set(null, new DummyConfig(dummyActivity));
        } catch (Exception e) { throw new RuntimeException(e); }
        picker.forResult(7);
    }

    @Test
    public void testFileInterceptor() {
        SImagePicker picker = SImagePicker.from(dummyActivity);
        FileChooseInterceptor inter = null;
        picker.fileInterceptor(inter);
    }
}