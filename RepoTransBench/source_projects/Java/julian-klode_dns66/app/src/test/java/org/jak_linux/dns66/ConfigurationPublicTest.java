package org.jak_linux.dns66;

import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.content.pm.ResolveInfo;
import android.util.Log;
import androidx.annotation.NonNull;

import org.hamcrest.CoreMatchers;
import org.junit.runner.RunWith;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.stubbing.Answer;

import java.io.IOException;
import java.io.StringReader;
import java.io.StringWriter;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.powermock.core.classloader.annotations.PrepareForTest;
import org.powermock.modules.junit4.PowerMockRunner;

import static org.junit.Assert.*;
import static org.mockito.Matchers.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;
import static org.powermock.api.mockito.PowerMockito.mockStatic;

/**
 * Public tests for Configuration with different test data
 */
@RunWith(PowerMockRunner.class)
@PrepareForTest(Log.class)
public class ConfigurationPublicTest {

    @Rule
    public ExpectedException thrown = ExpectedException.none();

    private Configuration.Item newItemForLocation(String location) {
        Configuration.Item item = new Configuration.Item();
        item.location = location;
        return item;
    }

    @Test
    public void testIsDownloadable() {
        try {
            newItemForLocation("").isDownloadable();
            fail("Was empty string");
        } catch (NullPointerException e) {
            // OK
        }

        assertTrue("http:// valid", newItemForLocation("http://public.com").isDownloadable());
        assertTrue("https:// valid", newItemForLocation("https://public.com").isDownloadable());
        assertFalse("ftp:// URI not downloadable", newItemForLocation("ftp://public.com").isDownloadable());
        assertFalse("file:///tmp/file", newItemForLocation("file:///tmp/file").isDownloadable());
        assertFalse("domain not downloadable", newItemForLocation("httpexample.com").isDownloadable());
        assertFalse("domain not downloadable", newItemForLocation("httpsexample.com").isDownloadable());
    }

    @Before
    public void setUp() {
        mockStatic(Log.class);
    }
    
    @Test
    public void testResolve() throws Exception {
        Configuration.Allowlist wl = new Configuration.Allowlist() {
            @Override
            Intent newBrowserIntent() {
                return mock(Intent.class);
            }
        };

        List<ResolveInfo> resolveInfoList = new ArrayList<>();
        List<ApplicationInfo> applicationInfoList = new ArrayList<>();

        // New public test data: different browser/app names
        resolveInfoList.add(newResolveInfo("public-system-browser", 0));
        applicationInfoList.add(newApplicationInfo("public-system-browser", ApplicationInfo.FLAG_SYSTEM));
        resolveInfoList.add(newResolveInfo("public-data-browser", 0));
        applicationInfoList.add(newApplicationInfo("public-data-browser", 0));

        // Not a browser
        applicationInfoList.add(newApplicationInfo("public-system-app", ApplicationInfo.FLAG_SYSTEM));
        applicationInfoList.add(newApplicationInfo("public-data-app", 0));

        // This app
        applicationInfoList.add(newApplicationInfo("org.jak_linux.dns66.public", 0));

        PackageManager pm = mock(PackageManager.class);
        //noinspection WrongConstant
        when(pm.queryIntentActivities(any(Intent.class), anyInt())).thenReturn(resolveInfoList);
        //noinspection WrongConstant
        when(pm.getInstalledApplications(anyInt())).thenReturn(applicationInfoList);

        Set<String> onVpn = new HashSet<>();
        Set<String> notOnVpn = new HashSet<>();

        wl.defaultMode = Configuration.Allowlist.DEFAULT_MODE_NOT_ON_VPN;
        wl.resolve(pm, onVpn, notOnVpn);

        assertTrue(notOnVpn.contains("public-system-app"));
        assertTrue(notOnVpn.contains("public-data-app"));
        assertTrue(notOnVpn.contains("public-system-browser"));
        assertTrue(notOnVpn.contains("public-data-browser"));

        // Default allow on vpn
        onVpn.clear();
        notOnVpn.clear();
        wl.defaultMode = Configuration.Allowlist.DEFAULT_MODE_ON_VPN;
        wl.resolve(pm, onVpn, notOnVpn);

        assertTrue(onVpn.contains("public-system-app"));
        assertTrue(onVpn.contains("public-data-app"));
        assertTrue(onVpn.contains("public-system-browser"));
        assertTrue(onVpn.contains("public-data-browser"));

        // Default intelligent on vpn
        onVpn.clear();
        notOnVpn.clear();
        wl.defaultMode = Configuration.Allowlist.DEFAULT_MODE_INTELLIGENT;
        wl.resolve(pm, onVpn, notOnVpn);

        assertTrue(notOnVpn.contains("public-system-app"));
        assertTrue(onVpn.contains("public-data-app"));
        assertTrue(onVpn.contains("public-system-browser"));
        assertTrue(onVpn.contains("public-data-browser"));

        // Default intelligent on vpn with custom items
        onVpn.clear();
        notOnVpn.clear();
        wl.items.clear();
        wl.itemsOnVpn.clear();
        wl.items.add("public-system-app");
        wl.items.add("public-data-browser");
        wl.defaultMode = Configuration.Allowlist.DEFAULT_MODE_INTELLIGENT;
        wl.resolve(pm, onVpn, notOnVpn);
        assertTrue(onVpn.contains("public-system-app"));
        assertTrue(notOnVpn.contains("public-data-browser"));

        // Check blacklisting with different app
        onVpn.clear();
        notOnVpn.clear();
        wl.items.clear();
        wl.itemsOnVpn.clear();
        wl.itemsOnVpn.add("public-data-app");
        wl.defaultMode = Configuration.Allowlist.DEFAULT_MODE_NOT_ON_VPN;
        wl.resolve(pm, onVpn, notOnVpn);
        assertTrue(onVpn.contains("public-data-app"));
    }

    @Test
    @PrepareForTest({Log.class})
    public void testRead() throws Exception {
        when(Log.d(anyString(), anyString(), any(Throwable.class))).then(new CountingAnswer(null));
        Configuration config = Configuration.read(new StringReader("{\"showNotification\":false,\"nightMode\":true}"));

        assertNotNull(config.hosts);
        assertNotNull(config.hosts.items);
        assertNotNull(config.allowlist);
        assertNotNull(config.allowlist.items);
        assertNotNull(config.allowlist.itemsOnVpn);
        assertNotNull(config.dnsServers);
        assertNotNull(config.dnsServers.items);
        assertTrue(config.ipV6Support);
        assertFalse(config.watchDog);
        assertTrue(config.nightMode);
        assertFalse(config.showNotification);
        assertFalse(config.autoStart);
    }

    @Test
    public void testReadNewer() throws Exception {
        thrown.expect(IOException.class);

        thrown.expectMessage(CoreMatchers.containsString("version"));
        Configuration.read(new StringReader("{version: " + (Configuration.VERSION + 2) + "}"));
    }

    @Test
    public void testReadWrite() throws Exception {
        Configuration config = Configuration.read(new StringReader("{\"autoStart\":true}"));
        StringWriter writer = new StringWriter();
        config.write(writer);
        Configuration config2 = Configuration.read(new StringReader(writer.toString()));
        StringWriter writer2 = new StringWriter();
        config2.write(writer2);
        assertEquals(writer.toString(), writer2.toString());
    }

    @NonNull
    private ResolveInfo newResolveInfo(String packageName, int flags) {
        ResolveInfo info = new ResolveInfo();
        info.activityInfo = new ActivityInfo();
        info.activityInfo.packageName = packageName;
        info.activityInfo.applicationInfo = new ApplicationInfo();
        info.activityInfo.applicationInfo.packageName = packageName;
        info.activityInfo.applicationInfo.flags = flags;
        return info;
    }

    @NonNull
    private ApplicationInfo newApplicationInfo(String packageName, int flags) {
        ApplicationInfo info = new ApplicationInfo();
        info.packageName = packageName;
        info.flags = flags;
        return info;
    }

    public class CountingAnswer implements Answer<Integer> {
        Integer value;

        public CountingAnswer(Integer ret) {
            value = ret;
        }

        @Override
        public Integer answer(InvocationOnMock invocation) throws Throwable {
            return value;
        }
    }
}