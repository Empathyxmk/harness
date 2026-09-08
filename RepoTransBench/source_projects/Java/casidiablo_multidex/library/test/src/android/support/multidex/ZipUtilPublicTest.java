package android.support.multidex;

import android.support.multidex.ZipUtil.CentralDirectory;
import org.junit.Assert;
import org.junit.BeforeClass;
import org.junit.Test;

import java.io.*;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.Map;
import java.util.zip.ZipEntry;
import java.util.zip.ZipException;
import java.util.zip.ZipFile;

public class ZipUtilPublicTest {
    // Use a dummy small zip file created for the public test so it differs from the internal one
    private static final File zipFile = createPublicTestZip();

    private static File createPublicTestZip() {
        try {
            File tempZip = File.createTempFile("ZipUtilPublicTest", ".zip");
            java.util.zip.ZipOutputStream zs = new java.util.zip.ZipOutputStream(new FileOutputStream(tempZip));
            ZipEntry entry1 = new ZipEntry("file1.txt");
            zs.putNextEntry(entry1);
            zs.write("hello".getBytes());
            zs.closeEntry();

            ZipEntry entry2 = new ZipEntry("file2.txt");
            zs.putNextEntry(entry2);
            zs.write("world".getBytes());
            zs.closeEntry();

            zs.close();
            tempZip.deleteOnExit();
            return tempZip;
        } catch (IOException e) {
            throw new RuntimeException("Could not create zip for public test", e);
        }
    }

    @BeforeClass
    public static void setupClass() throws ZipException, IOException {
        // just verify the zip is valid
        new ZipFile(zipFile).close();
    }

    @Test
    public void testCrcDoNotCrashPublic() throws IOException {
        long crc = ZipUtil.getZipCrc(zipFile);
        Assert.assertTrue(crc > 0);
    }

    @Test
    public void testCrcRangePublic() throws IOException {
        RandomAccessFile raf = new RandomAccessFile(zipFile, "r");
        CentralDirectory dir = ZipUtil.findCentralDirectory(raf);
        byte[] dirData = new byte[(int) dir.size];
        int length = dirData.length;
        int off = 0;
        raf.seek(dir.offset);
        while (length > 0) {
            int read = raf.read(dirData, off, length);
            if (read == -1) {
                throw new EOFException();
            }
            length -= read;
            off += read;
        }
        raf.close();
        ByteBuffer buffer = ByteBuffer.wrap(dirData);
        Map<String, ZipEntry> toCheck = new HashMap<String, ZipEntry>();
        // NOTE: this code uses a custom ZipEntryReader shipped with the library
        while (buffer.hasRemaining()) {
            buffer = buffer.slice();
            buffer.order(ByteOrder.LITTLE_ENDIAN);
            ZipEntry entry = ZipEntryReader.readEntry(buffer);
            toCheck.put(entry.getName(), entry);
        }

        ZipFile zip = new ZipFile(zipFile);
        Assert.assertEquals(zip.size(), toCheck.size());
        Enumeration<? extends ZipEntry> ref = zip.entries();
        while (ref.hasMoreElements()) {
            ZipEntry refEntry = ref.nextElement();
            ZipEntry checkEntry = toCheck.get(refEntry.getName());
            Assert.assertNotNull(checkEntry);
            Assert.assertEquals(refEntry.getName(), checkEntry.getName());
            Assert.assertEquals(refEntry.getComment(), checkEntry.getComment());
            Assert.assertEquals(refEntry.getTime(), checkEntry.getTime());
            Assert.assertEquals(refEntry.getCrc(), checkEntry.getCrc());
            Assert.assertEquals(refEntry.getCompressedSize(), checkEntry.getCompressedSize());
            Assert.assertEquals(refEntry.getSize(), checkEntry.getSize());
            Assert.assertEquals(refEntry.getMethod(), checkEntry.getMethod());
            Assert.assertArrayEquals(refEntry.getExtra(), checkEntry.getExtra());
        }
        zip.close();
    }

    @Test
    public void testCrcValuePublic() throws IOException {
        ZipFile zip = new ZipFile(zipFile);
        Enumeration<? extends ZipEntry> ref = zip.entries();
        byte[] buffer = new byte[0x2000];
        while (ref.hasMoreElements()) {
            ZipEntry refEntry = ref.nextElement();
            if (refEntry.getSize() > 0) {
                File tmp = File.createTempFile("ZipUtilPublicTest", ".fakezip");
                InputStream in = zip.getInputStream(refEntry);
                OutputStream out = new FileOutputStream(tmp);
                int read = in.read(buffer);
                while (read != -1) {
                    out.write(buffer, 0, read);
                    read = in.read(buffer);
                }
                in.close();
                out.close();
                RandomAccessFile raf = new RandomAccessFile(tmp, "r");
                CentralDirectory dir = new CentralDirectory();
                dir.offset = 0;
                dir.size = raf.length();
                long crc = ZipUtil.computeCrcOfCentralDir(raf, dir);
                Assert.assertEquals(refEntry.getCrc(), crc);
                raf.close();
                tmp.delete();
            }
        }
        zip.close();
    }

    @Test
    public void testInvalidCrcValuePublic() throws IOException {
        ZipFile zip = new ZipFile(zipFile);
        Enumeration<? extends ZipEntry> ref = zip.entries();
        byte[] buffer = new byte[0x2000];
        while (ref.hasMoreElements()) {
            ZipEntry refEntry = ref.nextElement();
            if (refEntry.getSize() > 0) {
                File tmp = File.createTempFile("ZipUtilPublicTest", ".fakezip");
                InputStream in = zip.getInputStream(refEntry);
                OutputStream out = new FileOutputStream(tmp);
                int read = in.read(buffer);
                while (read != -1) {
                    out.write(buffer, 0, read);
                    read = in.read(buffer);
                }
                in.close();
                out.close();
                RandomAccessFile raf = new RandomAccessFile(tmp, "r");
                CentralDirectory dir = new CentralDirectory();
                dir.offset = 0;
                dir.size = raf.length() - 2; // Differs: -2
                long crc = ZipUtil.computeCrcOfCentralDir(raf, dir);
                Assert.assertNotEquals(refEntry.getCrc(), crc);
                raf.close();
                tmp.delete();
            }
        }
        zip.close();
    }
}