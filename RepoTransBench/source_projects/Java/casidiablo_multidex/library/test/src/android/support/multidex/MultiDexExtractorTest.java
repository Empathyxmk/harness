package android.support.multidex;

import org.junit.Test;
import org.junit.Before;
import org.junit.After;
import static org.junit.Assert.*;

import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.content.SharedPreferences;

import java.io.File;
import java.io.IOException;
import java.util.List;

public class MultiDexExtractorTest {

    private static class MockApplicationInfo extends ApplicationInfo {
        public MockApplicationInfo(String sourceDir) {
            this.sourceDir = sourceDir;
        }
    }

    private File tempApk;

    @Before
    public void setUp() throws Exception {
        // create a temp file pretending to be APK
        tempApk = File.createTempFile("test", ".apk");
        tempApk.deleteOnExit();
        // Write basic zip header to avoid ZipException
        java.util.zip.ZipOutputStream zos = new java.util.zip.ZipOutputStream(new java.io.FileOutputStream(tempApk));
        zos.putNextEntry(new java.util.zip.ZipEntry("classes.dex"));
        zos.write("01234567".getBytes());
        zos.closeEntry();
        zos.close();
    }

    @Test
    public void testLoadWithNoSecondaryDex() throws Exception {
        Context ctx = new android.test.mock.MockContext();
        ApplicationInfo info = new MockApplicationInfo(tempApk.getAbsolutePath());
        File dexDir = new File(System.getProperty("java.io.tmpdir"));
        List<File> files = MultiDexExtractor.load(ctx, info, dexDir, false);
        // Should not fail, may return empty or non-empty list depending on APK simulated content
        assertNotNull(files);
    }

    @Test(expected = IOException.class)
    public void testBadZipCrcFileThrows() throws Exception {
        File fake = File.createTempFile("fake", ".apk");
        fake.deleteOnExit();
        // Not a valid zip, should cause CRC to throw
        Context ctx = new android.test.mock.MockContext();
        ApplicationInfo info = new MockApplicationInfo(fake.getAbsolutePath());
        MultiDexExtractor.load(ctx, info, fake.getParentFile(), false);
    }

    @After
    public void tearDown() {
        if (tempApk != null && tempApk.exists()) tempApk.delete();
    }
}