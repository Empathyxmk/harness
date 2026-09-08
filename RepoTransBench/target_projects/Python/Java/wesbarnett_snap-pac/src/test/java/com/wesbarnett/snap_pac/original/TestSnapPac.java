package com.wesbarnett.snap_pac.original;

import com.wesbarnett.snap_pac.scripts.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import org.mockito.Mockito;

class TestSnapPac {

    static class DummyPopenResult extends InputStream {
        private final String value;
        private int index = 0;

        DummyPopenResult(String ret) { this.value = ret; }

        @Override
        public int read() throws IOException {
            if (index >= value.length())
                return -1;
            return value.charAt(index++);
        }

        public String readLine() {
            return value;
        }
    }

    @Test
    void testSnapperCmdStrAndCall() throws Exception {
        SnapperCmd cmd = new SnapperCmd("root", "pre", "number", "desc", true, 123, "ud");
        String s = cmd.toString();
        assertTrue(s.contains("--no-dbus"));
        assertTrue(s.contains("--config root create"));
        assertTrue(s.contains("--description \"desc\""));
        assertTrue(s.contains("--userdata \"ud\""));
        assertTrue(s.contains("--type pre"));
        // Simulate os.popen: SnapperCmd.__call__ reads from popen
        cmd.setPopenSupplier((c) -> new DummyPopenResult("42\n"));
        String result = cmd.call();
        assertEquals("42", result.strip());
    }

    @Test
    void testSnapperCmdPostNoPrenumber() throws Exception {
        SnapperCmd cmd = new SnapperCmd("root", "post", "number", null, false, null, null);
        String strCmd = cmd.toString();
        boolean contains = strCmd.contains("--type single") || strCmd.contains("--type post");
        assertTrue(contains);
        cmd.setPopenSupplier((c) -> new DummyPopenResult("test"));
        cmd.call();
    }

    @Test
    void testConfigProcessorDefaultSettings() throws Exception {
        Path ini = Files.createTempFile("config", ".ini");
        Files.writeString(ini, "");
        ConfigProcessor cp = new ConfigProcessor(ini.toString(), "pre", "parent", Arrays.asList("pkg1", "pkg2"));
        Map<String, Object> result = cp.apply("root");
        assertTrue(result.get("description").toString().startsWith("parent"));
        assertEquals("number", result.get("cleanup_algorithm"));
    }

    @Test
    void testConfigProcessorIniOptions() throws Exception {
        Path ini = Files.createTempFile("ext", ".ini");
        String config_txt = """
[DEFAULT]
snapshot = false
cleanup_algorithm = timeline
pre_description = mycmd
post_description = install packages
desc_limit = 5
important_packages = ["imp"]
important_commands = ["imp_cmd"]
userdata = ["mytag"]
[root]
snapshot = true
""";
        Files.writeString(ini, config_txt);
        ConfigProcessor cp = new ConfigProcessor(ini.toString(), "pre", "imp_cmd", Arrays.asList("imp", "unimp"));
        assertEquals("timeline", cp.getCleanupAlgorithm("root"));
        assertEquals("mycmd", cp.getDescription("root"));
        assertTrue(cp.checkImportantCommands("root"));
        assertTrue(cp.checkImportantPackages("root"));
        String ud = cp.getUserdata("root");
        assertTrue(ud.contains("important=yes") && ud.contains("mytag"));
        Map<String, Object> out = cp.apply("root");
        assertTrue(out.containsKey("description"));
        assertTrue(out.containsKey("userdata"));
    }

    @Test
    void testConfigProcessorNonexistentSection() throws Exception {
        Path ini = Files.createTempFile("spawn", ".ini");
        Files.writeString(ini, "");
        ConfigProcessor cp = new ConfigProcessor(ini.toString(), "post", "irrelevant", List.of());
        Map<String, Object> rv = cp.apply("not_here");
        assertTrue(rv instanceof Map);
        assertTrue(rv.get("snapshot").equals(Boolean.FALSE) || rv.get("snapshot").equals(Boolean.TRUE));
    }

    @Test
    void testConfigProcessorCheckImportant() throws Exception {
        Path ini = Files.createTempFile("imp2", ".ini");
        Files.writeString(ini, """
[root]
snapshot = true
important_packages = ["pkgx"]
important_commands = ["cmdy"]
userdata = ["z"]
""");
        ConfigProcessor cp = new ConfigProcessor(ini.toString(), "post", "cmdy", Arrays.asList("pkgx", "pkgother"));
        boolean rv = cp.checkImportant("root");
        assertTrue(rv);
    }

    @Test
    void testConfigProcessorNoImportant() throws Exception {
        Path ini = Files.createTempFile("noimp", ".ini");
        Files.writeString(ini, """
[root]
snapshot = true
important_packages = []
important_commands = []
userdata = []
""");
        ConfigProcessor cp = new ConfigProcessor(ini.toString(), "post", "foo", Arrays.asList("bar"));
        assertFalse(cp.checkImportant("root"));
        assertFalse(cp.getUserdata("root").contains("important=yes"));
    }

    @Test
    void testSnapperCmdTypes() {
        SnapperCmd cmd = new SnapperCmd("abc", "post", "alg", null, false, null, null);
        String out = cmd.toString();
        assertTrue(out.contains("--type single") || out.contains("--type post"));
    }
}