package org.csource.fastdfs;

import org.junit.Test;

import java.util.Date;

import static org.junit.Assert.*;

public class FileInfoTest {

    @Test
    public void testConstructorAndGetters() {
        FileInfo fileInfo = new FileInfo(true, FileInfo.FILE_TYPE_NORMAL, 123456789L, 1609459200, 0xAABBCCDD, "127.0.0.1");
        assertTrue(fileInfo.getFetchFromServer());
        assertEquals(FileInfo.FILE_TYPE_NORMAL, fileInfo.getFileType());
        assertEquals(123456789L, fileInfo.getFileSize());
        assertEquals("127.0.0.1", fileInfo.getSourceIpAddr());
        assertEquals(0xAABBCCDDL, fileInfo.getCrc32());

        // Date for 1609459200 (2021-01-01 00:00:00 UTC)
        Date expectedDate = new Date(1609459200L * 1000L);
        assertEquals(expectedDate, fileInfo.getCreateTimestamp());
    }

    @Test
    public void testSetters() {
        FileInfo fileInfo = new FileInfo(false, FileInfo.FILE_TYPE_APPENDER, 0, 0, 0, "");
        fileInfo.setFetchFromServer(true);
        fileInfo.setFileType(FileInfo.FILE_TYPE_SLAVE);
        fileInfo.setSourceIpAddr("192.168.100.100");
        fileInfo.setFileSize(1000000L);
        fileInfo.setCreateTimestamp(1620000000);
        fileInfo.setCrc32(0xFFFFEEEE);

        assertTrue(fileInfo.getFetchFromServer());
        assertEquals(FileInfo.FILE_TYPE_SLAVE, fileInfo.getFileType());
        assertEquals("192.168.100.100", fileInfo.getSourceIpAddr());
        assertEquals(1000000L, fileInfo.getFileSize());
        assertEquals(new Date(1620000000L * 1000L), fileInfo.getCreateTimestamp());
        assertEquals(0xFFFFEEEEL, fileInfo.getCrc32());
    }

    @Test
    public void testToStringFormat() {
        FileInfo fileInfo = new FileInfo(false, FileInfo.FILE_TYPE_NORMAL, 1, 1, 111, "10.0.0.1");
        String str = fileInfo.toString();
        assertTrue(str.contains("fetch_from_server"));
        assertTrue(str.contains("file_type"));
        assertTrue(str.contains("source_ip_addr"));
        assertTrue(str.contains("file_size"));
        assertTrue(str.contains("crc32"));
        assertTrue(str.contains("create_timestamp"));
    }
}