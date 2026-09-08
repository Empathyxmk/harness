package com.ecmwf.ai_models.original;

import org.junit.jupiter.api.*;
import org.mockito.Mockito;

import com.ecmwf.ai_models.checkpoint.Checkpoint;
import com.ecmwf.ai_models.checkpoint.Checkpoint.FakeStorage;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import java.util.HashMap;
import java.util.zip.*;
import java.util.UUID;
import java.util.List;
import java.util.ArrayList;

class CheckpointTest {

    @Test
    void test_tidy_dict_and_list_tuple() {
        // Java doesn't distinguish, so simple test
        Map<String, Object> d = new HashMap<>();
        List<Object> aList = new ArrayList<>();
        aList.add(1);
        aList.add(2);
        Map<String, Object> inner = new HashMap<>();
        Object[] btup = new Object[]{3, null};
        inner.put("b", btup);
        aList.add(inner);
        d.put("a", aList);
        d.put("c", new Object[]{4, 5});

        Object result = Checkpoint.tidy(d);
        Assertions.assertEquals(d, result);
    }

    @Test
    void test_tidy_base_types() {
        for (Object val : new Object[]{null, 3, 0.1, "foo", true}) {
            Assertions.assertEquals(val, Checkpoint.tidy(val));
        }
    }

    @Test
    void test_tidy_unknown_type() {
        Object foo = new Object();
        Assertions.assertEquals(foo, Checkpoint.tidy(foo));
    }

    @Test
    void test_FakeStorage_construction() {
        FakeStorage s = new FakeStorage();
        Assertions.assertNotNull(s.dtype);
        Assertions.assertNotNull(s);
    }

    @Test
    void test_UnpicklerWrapper() {
        // Simulate persistent load
        Checkpoint.UnpicklerWrapper uw = new Checkpoint.UnpicklerWrapper(new byte[]{});
        Object res = uw.persistentLoad("id");
        Assertions.assertTrue(res instanceof FakeStorage);
    }

    private String makeZipWithDataPkl(Map<String, Object> obj, String filename, boolean extra) throws IOException {
        File tempFile = File.createTempFile("chkpt", ".zip");
        tempFile.deleteOnExit();
        try (ZipOutputStream zos = new ZipOutputStream(new FileOutputStream(tempFile))) {
            ZipEntry ent = new ZipEntry(filename);
            zos.putNextEntry(ent);
            // Use ObjectOutputStream just for placeholder. In real, should serialize.
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(baos);
            oos.writeObject(obj);
            oos.close();
            byte[] bytes = baos.toByteArray();
            zos.write(bytes, 0, bytes.length);
            if (extra) {
                ZipEntry ent2 = new ZipEntry("data2.pkl");
                zos.putNextEntry(ent2);
                zos.write("data2".getBytes());
            }
        }
        return tempFile.getAbsolutePath();
    }

    @Test
    void test_peek_single_data_pkl() throws Exception {
        Map<String, Object> m = new HashMap<>();
        m.put("foo", 1);
        String zfile = makeZipWithDataPkl(m, "data.pkl", false);
        Object result = Checkpoint.peek(zfile);
        Assertions.assertTrue(result instanceof Map);
        Assertions.assertEquals(1, ((Map<?, ?>) result).get("foo"));
        Files.deleteIfExists(Path.of(zfile));
    }

    @Test
    void test_peek_duplicate_data_pkl() throws Exception {
        File tempFile = File.createTempFile("chkpt", ".zip");
        tempFile.deleteOnExit();
        try (ZipOutputStream zos = new ZipOutputStream(new FileOutputStream(tempFile))) {
            Map<String, Object> first = new HashMap<>();
            first.put("x", 1);
            Map<String, Object> second = new HashMap<>();
            second.put("y", 2);
            // Write two data.pkl entries in different dirs
            ByteArrayOutputStream baos1 = new ByteArrayOutputStream();
            ObjectOutputStream oos1 = new ObjectOutputStream(baos1);
            oos1.writeObject(first);
            oos1.close();
            byte[] bytes1 = baos1.toByteArray();

            ByteArrayOutputStream baos2 = new ByteArrayOutputStream();
            ObjectOutputStream oos2 = new ObjectOutputStream(baos2);
            oos2.writeObject(second);
            oos2.close();
            byte[] bytes2 = baos2.toByteArray();

            zos.putNextEntry(new ZipEntry("first/data.pkl"));
            zos.write(bytes1);
            zos.putNextEntry(new ZipEntry("second/data.pkl"));
            zos.write(bytes2);
        }
        Exception exc = Assertions.assertThrows(Exception.class, () -> {
            Checkpoint.peek(tempFile.getAbsolutePath());
        });
        Assertions.assertTrue(exc.getMessage().contains("Found two data.pkl"));
        Files.deleteIfExists(tempFile.toPath());
    }

}