package com.imnjh.imagepicker;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.net.Uri;
import android.os.Environment;
import android.support.v4.app.Fragment;

import org.junit.*;
import org.junit.rules.TemporaryFolder;

import java.io.File;
import java.util.*;

import static org.junit.Assert.*;

public class CapturePhotoHelperPublicTest {

    static class DummyActivity extends Activity {
        public Intent lastIntent = null;
        public int lastRequestCode = -1;
        public PackageManager pkgMgr;
        public DummyActivity(PackageManager pm) { pkgMgr = pm;}
        @Override
        public void startActivityForResult(Intent intent, int requestCode) {
            lastIntent = intent;
            lastRequestCode = requestCode;
        }
        @Override
        public PackageManager getPackageManager() { return pkgMgr; }
        @Override
        public Context getApplicationContext() { return this; }
    }

    static class DummyFragment extends Fragment {
        public Intent lastIntent;
        public int lastRequestCode;
        private final DummyActivity activity;
        DummyFragment(DummyActivity act) { activity = act; }
        @Override
        public void startActivityForResult(Intent intent, int requestCode) {
            lastIntent = intent;
            lastRequestCode = requestCode;
        }
        @Override
        public Activity getActivity() { return activity; }
        @Override
        public Context getContext() { return activity; }
    }

    static class DummyPackageManager extends PackageManager {
        List<ResolveInfo> acts;
        DummyPackageManager(List<ResolveInfo> l) {acts = l;}
        @Override
        public List<ResolveInfo> queryIntentActivities(Intent intent, int flags) { return acts; }
        // Implement abstract methods as needed with dummy logic.
    }

    @Rule public TemporaryFolder temp = new TemporaryFolder();

    DummyPackageManager withCamera;
    DummyPackageManager withoutCamera;
    DummyActivity dummyAct;
    DummyFragment dummyFrag;

    @Before
    public void setup() {
        // Use two resolve infos to differentiate from existing test
        withCamera = new DummyPackageManager(Arrays.asList(new ResolveInfo(), new ResolveInfo()));
        withoutCamera = new DummyPackageManager(Collections.emptyList());
        dummyAct = new DummyActivity(withCamera);
        dummyFrag = new DummyFragment(dummyAct);
    }

    @Test
    public void testHasCameraTrueAndFalse_public() {
        CapturePhotoHelper hpAct = new CapturePhotoHelper(dummyAct);
        assertTrue(hpAct.hasCamera());

        DummyActivity noCamAct = new DummyActivity(withoutCamera);
        CapturePhotoHelper hpNoCam = new CapturePhotoHelper(noCamAct);
        assertFalse(hpNoCam.hasCamera());
    }

    @Test
    public void testSetPhotoAndGetPhoto_public() {
        CapturePhotoHelper hp = new CapturePhotoHelper(dummyAct);
        String filePath = temp.getRoot().getAbsolutePath() + "/unique_img.png";
        hp.setPhoto(filePath);
        File file = hp.getPhoto();
        assertEquals(filePath, file.getAbsolutePath());
    }

    @Test
    public void testCreatePhotoFileFallback_public() throws Exception {
        CapturePhotoHelper hp = new CapturePhotoHelper(dummyAct);
        // Force photoFolder null for branch
        java.lang.reflect.Field pf = CapturePhotoHelper.class.getDeclaredField("photoFolder");
        pf.setAccessible(true);
        pf.set(hp, null);
        java.lang.reflect.Method meth = CapturePhotoHelper.class.getDeclaredMethod("createPhotoFile");
        meth.setAccessible(true);
        meth.invoke(hp);
        assertNull(hp.getPhoto());
    }

    // capturePhoto() with another uri
    @Test
    public void testCapturePhoto_withUri_public() {
        CapturePhotoHelper hpFrag = new CapturePhotoHelper(dummyFrag);
        Uri uri = Uri.parse("content://different/path");
        hpFrag.capturePhoto(uri);
        assertNotNull(dummyFrag.lastIntent);
        assertEquals(CapturePhotoHelper.CAPTURE_PHOTO_REQUEST_CODE, dummyFrag.lastRequestCode);

        CapturePhotoHelper hpAct = new CapturePhotoHelper(dummyAct);
        dummyAct.lastIntent = null;
        hpAct.capturePhoto(uri);
        assertNotNull(dummyAct.lastIntent);
        assertEquals(CapturePhotoHelper.CAPTURE_PHOTO_REQUEST_CODE, dummyAct.lastRequestCode);
    }

    @Test
    public void testCapturePhoto_nullUri_public() {
        CapturePhotoHelper hp = new CapturePhotoHelper(dummyAct);
        // Should do nothing, just not crash
        hp.capturePhoto(null);
        assertNull(dummyAct.lastIntent);
    }
}