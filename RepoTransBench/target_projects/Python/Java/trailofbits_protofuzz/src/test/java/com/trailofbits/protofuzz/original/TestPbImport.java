package com.trailofbits.protofuzz.original;

import org.junit.jupiter.api.Test;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public class TestPbImport {

    static class ProtoModule {
        // Simulate a proto module with a DESCRIPTOR field
        public static final String DESCRIPTOR = "dummy";
    }

    public static ProtoModule importProtoModule(String path) {
        // mock
        return new ProtoModule();
    }

    public static String resolveIncludePath(String fileName, List<String> searchPaths) {
        for (String dir : searchPaths) {
            File file = new File(dir, fileName);
            if (file.exists()) {
                return file.getAbsolutePath();
            }
        }
        return null;
    }

    public static java.util.List<String> parseProtoImports(String text) {
        java.util.List<String> result = new java.util.ArrayList<>();
        String[] lines = text.split("\\n");
        for (String line : lines) {
            line = line.trim();
            if (line.startsWith("import")) {
                int start = line.indexOf("\"");
                int end = line.lastIndexOf("\"");
                if (start >= 0 && end > start) {
                    result.add(line.substring(start + 1, end));
                }
            }
        }
        return result;
    }

    @Test
    public void testImportProtoModuleSmoke() {
        ProtoModule module = importProtoModule("some/path/to/test.proto");
        assertNotNull(module);
        assertEquals("dummy", module.DESCRIPTOR);
    }

    @Test
    public void testResolveIncludePathExists() throws IOException {
        File tmpDir = Files.createTempDirectory("testpbimport").toFile();
        tmpDir.deleteOnExit();
        File testProto = new File(tmpDir, "abc.proto");
        testProto.createNewFile();
        testProto.deleteOnExit();
        assertEquals(testProto.getAbsolutePath(),
                resolveIncludePath("abc.proto", java.util.Collections.singletonList(tmpDir.getAbsolutePath())));
    }

    @Test
    public void testResolveIncludePathNotFound() throws IOException {
        File tmpDir = Files.createTempDirectory("testpbnotfound").toFile();
        tmpDir.deleteOnExit();
        assertNull(resolveIncludePath("idontexist.proto", java.util.Collections.singletonList(tmpDir.getAbsolutePath())));
    }

    @Test
    public void testParseProtoImportsSimple() {
        String text = "import \"foo.proto\";\n";
        List<String> result = parseProtoImports(text);
        assertTrue(result.contains("foo.proto"));
    }
}