package com.wesbarnett.snap_pac.public_tests;

import com.wesbarnett.snap_pac.scripts.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.nio.file.*;
import java.util.*;

class PublicTestSnapPac {

    static class DummyPopenResult extends InputStream {
        private final String value;
        private int index = 0;
        DummyPopenResult(String ret) { this.value = ret; }
        @Override
        public int read() {
            if (index >= value.length()) return -1;
            return value.charAt(index++);
        }
        public String readLine() { return value; }
    }

    @Test
    void testPublicSnapperCmdStrAndCall() {
        SnapperCmd cmd = new SnapperCmd("data", "pre", "timeline", "my-desc", true, 789, "user_data");
        String s = cmd.toString();
        assertTrue(s.contains("--no-dbus"));
        assertTrue(s.contains("--config data create"));
        assertTrue(s.contains("--description \"my-desc\""));
        assertTrue(s.contains("--userdata \"user_data\""));
        assertTrue(s.contains("--type pre"));

        cmd.setPopenSupplier((c) -> new DummyPopenResult("314\n"));
        String result = cmd.call();
        assertEquals("314", result.strip());
    }

    @Test
    void testPublicSnapperCmdPostNoPrenumber() {
        SnapperCmd cmd = new SnapperCmd("foo", "post", "timeline", null, false, null, null);
        String strCmd = cmd.toString();
        boolean contains = strCmd.contains("--type single") || strCmd.contains("--type post");
        assertTrue(contains);
        cmd.setPopenSupplier((c) -> new DummyPopenResult("returnz"));
        cmd.call();
    }

    @Test
    void testPublicConfigProcessorDefaultSettings() throws Exception {
        Path ini = Files.createTempFile("another_config", ".ini");
        Files.writeString(ini, "");
        ConfigProcessor cp = new ConfigProcessor(ini.toString(), "post", "runjob", Arrays.asList("abc", "xyz"));
        Map<String, Object> result = cp.apply("home");
        String desc = (String) result.get("description");
        assertTrue(desc.startsWith("abc") || desc.startsWith("runjob") || desc.startsWith("xyz"));
        assertEquals("number", result.get("cleanup_algorithm"));
    }

    @Test
    void testPublicConfigProcessorIniOptions() throws Exception {
        Path ini = Files.createTempFile("more", ".ini");
        String config_txt = """
[DEFAULT]
snapshot = true
cleanup_algorithm = number
pre_description = commandX
post_description = just_test
desc_limit = 6
important_packages = ["abc"]
important_commands = ["ccc"]
userdata = ["newtag"]
[home]
snapshot = false
""";
        Files.writeString(ini, config_txt);
        ConfigProcessor cp = new ConfigProcessor(ini.toString(), "pre", "ccc", Arrays.asList("abc", "wxy"));
        assertEquals("number", cp.getCleanupAlgorithm("home"));
        assertEquals("comman", cp.getDescription("home"));
        assertTrue(cp.checkImportantCommands("home"));
        assertTrue(cp.checkImportantPackages("home"));
        String ud = cp.getUserdata("home");
        assertTrue(ud.contains("important=yes") && ud.contains("newtag"));
        Map<String, Object> out = cp.apply("home");
        assertTrue(out.containsKey("description"));
        assertTrue(out.containsKey("userdata"));
    }

    @Test
    void testPublicConfigProcessorNonexistentSection() throws Exception {
        Path ini = Files.createTempFile("section", ".ini");
        Files.writeString(ini, "");
        ConfigProcessor cp = new ConfigProcessor(ini.toString(), "pre", "diff", List.of());
        Map<String, Object> rv = cp.apply("qwerty");
        assertTrue(rv instanceof Map);
        assertTrue(rv.containsKey("snapshot"));
    }

    @Test
    void testPublicConfigProcessorCheckImportant() throws Exception {
        Path ini = Files.createTempFile("zzz", ".ini");
        Files.writeString(ini, """
[home]
snapshot = false
important_packages = ["specialpkg"]
important_commands = ["specialcmd"]
userdata = ["t"]
""");
        ConfigProcessor cp = new ConfigProcessor(ini.toString(), "post", "specialcmd", Arrays.asList("specialpkg", "otherpkg"));
        assertTrue(cp.checkImportant("home"));
    }

    @Test
    void testPublicConfigProcessorNoImportant() throws Exception {
        Path ini = Files.createTempFile("notag", ".ini");
        Files.writeString(ini, """
[zzz]
snapshot = false
important_packages = []
important_commands = []
userdata = []
""");
        ConfigProcessor cp = new ConfigProcessor(ini.toString(), "post", "nope", Arrays.asList("nil"));
        assertFalse(cp.checkImportant("zzz"));
        assertFalse(cp.getUserdata("zzz").contains("important=yes"));
    }

    @Test
    void testPublicSnapperCmdTypes() {
        SnapperCmd cmd = new SnapperCmd("customcfg", "post", "otheralg", null, false, null, null);
        String out = cmd.toString();
        assertTrue(out.contains("--type single") || out.contains("--type post"));
    }
}