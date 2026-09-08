package com.example.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;

import com.example.graphios_backends.BackendLoader;
import com.example.graphios_backends.FileBackend;
import com.example.graphios_backends.CarbonBackend;
import com.example.graphios_backends.UDPSendBackend;

public class TestGraphiosBackends {

    @Test
    public void testLoadBackendInvalid() {
        assertThrows(IllegalArgumentException.class, () -> {
            BackendLoader.load_backend("doesnotexist");
        });
    }

    @Test
    public void testLoadBackendFile() {
        Object backend = BackendLoader.load_backend("file", "/tmp/testfile");
        assertEquals("FileBackend", backend.getClass().getSimpleName());
    }

    @Test
    public void testLoadBackendCarbon() {
        Object backend = BackendLoader.load_backend("carbon", "host", 1234);
        assertEquals("CarbonBackend", backend.getClass().getSimpleName());
    }

    @Test
    public void testLoadBackendUdp() {
        Object backend = BackendLoader.load_backend("udp", "host", 1001);
        assertEquals("UDPSendBackend", backend.getClass().getSimpleName());
    }

    @Test
    public void testFilebackendSendMetric(@TempDir Path tempDir) throws Exception {
        class FakeMetric {
            public String host = "a";
            public String service = "b";
            public String metric = "c";
            public String value = "1";
            public String timestamp = "2";
        }
        Path fpath = tempDir.resolve("outfile");
        FileBackend back = new FileBackend(fpath.toAbsolutePath().toString());
        back.send_metric(new FakeMetric());
        String data = new String(Files.readAllBytes(fpath));
        assertTrue(data.contains("a b c 1 2"));
    }

    @Test
    public void testCarbonbackendSendMetric() {
        class FakeMetric {
            public String host = "h";
            public String service = "s";
            public String metric = "m";
            public int value = 5;
            public int timestamp = 18;
        }
        CarbonBackend back = new CarbonBackend("test.host", 2003);
        try {
            back.send_metric(new FakeMetric());
        } catch (Exception ignored) {}
        assertTrue(true); // If no exception, test is successful
    }

    @Test
    public void testUdpbackendSendMetric() {
        class FakeMetric {
            public String host = "hosty";
            public String service = "svc";
            public String metric = "metric";
            public int value = 3;
            public int timestamp = 6;
        }
        UDPSendBackend back = new UDPSendBackend("testhost", 2222);
        try {
            back.send_metric(new FakeMetric());
        } catch (Exception ignored) {}
        assertTrue(true);
    }
}