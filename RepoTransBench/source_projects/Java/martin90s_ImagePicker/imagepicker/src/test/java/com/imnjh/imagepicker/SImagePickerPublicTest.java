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

public class SImagePickerPublicTest {

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
    public void testGetPickerConfig_exceptionIfNotInitialized_public() {
        SImagePicker picker = SImagePicker.from(dummyActivity);
        try {
            java.lang.reflect.Field field = SImagePicker.class.getDeclaredField("pickerConfig");
            field.setAccessible(true);
            field.set(null, null);
        } catch (Exception e) { throw new RuntimeException(e); }
        SImagePicker.getPickerConfig();
    }

    @Test(expected = IllegalArgumentException.class)
    public void testForResult_noInit_throws_public() {
        try {
            java.lang.reflect.Field field = SImagePicker.class.getDeclaredField("pickerConfig");
            field.setAccessible(true);
            field.set(null, null);
        } catch (Exception e) { throw new RuntimeException(e); }
        SImagePicker picker = SImagePicker.from(dummyActivity);
        picker.forResult(11);
    }

    @Test
    public void testFromActivityAndFromFragment_public() {
        SImagePicker picker1 = SImagePicker.from(dummyActivity);
        assertNotNull(picker1);
        SImagePicker picker2 = SImagePicker.from(dummyFragment);
        assertNotNull(picker2);
    }

    @Test
    public void testMaxCountRowCountPickModeCropFileShowCameraPickTextSetSelected_public() {
        SImagePicker picker = SImagePicker.from(dummyActivity);
        ArrayList<String> selected = new ArrayList<>();
        selected.add("abc");
        picker.maxCount(3).rowCount(5).pickMode(SImagePicker.MODE_IMAGE)
                .cropFilePath("other_file.png").showCamera(false).pickText(456)
                .setSelected(selected);
    }

    @Test
    public void testForResultCallsActivityAndFragment_public() {
        SImagePicker pickerA = SImagePicker.from(dummyActivity);
        pickerA.forResult(42);
        assertNotNull(dummyActivity.lastIntent);
        assertEquals(42, dummyActivity.lastRequestCode);

        SImagePicker pickerF = SImagePicker.from(dummyFragment);
        pickerF.forResult(24);
        assertNotNull(dummyFragment.lastIntent);
        assertEquals(24, dummyFragment.lastRequestCode);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testForResult_neitherActivityNorFragment_public() {
        SImagePicker picker = new SImagePicker(null) {
        };
        try {
            java.lang.reflect.Field f = SImagePicker.class.getDeclaredField("pickerConfig");
            f.setAccessible(true);
            f.set(null, new DummyConfig(dummyActivity));
        } catch (Exception e) { throw new RuntimeException(e); }
        picker.forResult(999);
    }

    @Test
    public void testFileInterceptor_public() {
        SImagePicker picker = SImagePicker.from(dummyActivity);
        FileChooseInterceptor inter = new FileChooseInterceptor() {
            @Override public boolean onFileChosen(Context context, ArrayList<String> sel, boolean orig, int code, PickerAction action) {return true;}
            @Override public int describeContents() { return 0; }
            @Override public void writeToParcel(android.os.Parcel dest, int flags) {}
        };
        picker.fileInterceptor(inter);
    }
}