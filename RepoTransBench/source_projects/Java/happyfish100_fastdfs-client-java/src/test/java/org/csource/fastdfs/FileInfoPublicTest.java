package org.csource.fastdfs;

import org.junit.Test;

import java.util.Date;

import static org.junit.Assert.*;

public class FileInfoPublicTest {

    @Test
    public void testConstructorAndGettersPublic() {
        // Different file size, IP, CRC, timestamp
        FileInfo fileInfo = new FileInfo(false, FileInfo.FILE_TYPE_SLAVE, 987654321L, 1672531200, 0xBBCCDDEE, "192.168.1.1");
        assertFalse(fileInfo.getFetchFromServer());
        assertEquals(FileInfo.FILE_TYPE_SLAVE, fileInfo.getFileType());
        assertEquals(987654321L, fileInfo.getFileSize());
        assertEquals("192.168.1.1", fileInfo.getSourceIpAddr());
        assertEquals(0xBBCCDDEEL, fileInfo.getCrc32());

        // Date for 1672531200 (2023-01-01 00:00:00 UTC)
        Date expectedDate = new Date(1672531200L * 1000L);
        assertEquals(expectedDate, fileInfo.getCreateTimestamp());
    }

    @Test
    public void testSettersPublic() {
        FileInfo fileInfo = new FileInfo(true, FileInfo.FILE_TYPE_NORMAL, 0, 0, 0, "");
        fileInfo.setFetchFromServer(false);
        fileInfo.setFileType(FileInfo.FILE_TYPE_APPENDER);
        fileInfo.setSourceIpAddr("10.1.2.3");
        fileInfo.setFileSize(1234567L);
        fileInfo.setCreateTimestamp(1680000000);
        fileInfo.setCrc32(0xABCDEFFF);

        assertFalse(fileInfo.getFetchFromServer());
        assertEquals(FileInfo.FILE_TYPE_APPENDER, fileInfo.getFileType());
        assertEquals("10.1.2.3", fileInfo.getSourceIpAddr());
        assertEquals(1234567L, fileInfo.getFileSize());
        assertEquals(new Date(1680000000L * 1000L), fileInfo.getCreateTimestamp());
        assertEquals(0xABCDEFFFL, fileInfo.getCrc32());
    }

    @Test
    public void testToStringFormatPublic() {
        FileInfo fileInfo = new FileInfo(true, FileInfo.FILE_TYPE_SLAVE, 2, 2, 222, "172.16.100.200");
        String str = fileInfo.toString();
        assertTrue(str.contains("fetch_from_server"));
        assertTrue(str.contains("file_type"));
        assertTrue(str.contains("source_ip_addr"));
        assertTrue(str.contains("file_size"));
        assertTrue(str.contains("crc32"));
        assertTrue(str.contains("create_timestamp"));
    }
}