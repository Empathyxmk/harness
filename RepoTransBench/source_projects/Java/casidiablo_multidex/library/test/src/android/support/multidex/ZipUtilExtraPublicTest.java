package android.support.multidex;

import org.junit.Assert;
import org.junit.Test;

import java.util.zip.ZipEntry;

public class ZipUtilExtraPublicTest {
    @Test
    public void testZipEntryNoExtraDataPublic() {
        ZipEntry entry = new ZipEntry("anotherfile.txt");
        Assert.assertNull(entry.getExtra());
        entry.setExtra(new byte[0]);
        Assert.assertNotNull(entry.getExtra());
        Assert.assertEquals(0, entry.getExtra().length);
    }

    @Test
    public void testZipEntryWithExtraDataPublic() {
        ZipEntry entry = new ZipEntry("some_entry.txt");
        byte[] extra = new byte[] {42, 7, 100, 5};
        entry.setExtra(extra);
        Assert.assertArrayEquals(extra, entry.getExtra());
    }
}