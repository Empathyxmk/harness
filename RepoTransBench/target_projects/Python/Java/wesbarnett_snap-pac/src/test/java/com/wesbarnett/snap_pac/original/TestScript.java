package com.wesbarnett.snap_pac.original;

import com.wesbarnett.snap_pac.scripts.*;
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.*;
import org.junit.jupiter.params.provider.*;
import java.util.*;
import java.io.*;
import java.nio.file.*;
import static org.junit.jupiter.api.Assertions.*;

class TestScript {

    static class SnapperCmdCase {
        SnapperCmd cmd;
        String expected;
        SnapperCmdCase(SnapperCmd cmd, String expected) {
            this.cmd = cmd;
            this.expected = expected;
        }
    }

    static Stream<Arguments> snapperCmdProvider() {
        return Stream.of(
                Arguments.of(
                        new SnapperCmd("root", "pre", "number", "foo"),
                        "snapper --config root create --cleanup-algorithm number --print-number --description \"foo\" --type pre"
                ),
                Arguments.of(
                        new SnapperCmd("root", "post", "number", "bar", false, 1234),
                        "snapper --config root create --cleanup-algorithm number --print-number --description \"bar\" --pre-number 1234 --type post"
                ),
                Arguments.of(
                        new SnapperCmd("root", "post", "number", "bar", true, 1234),
                        "snapper --no-dbus --config root create --cleanup-algorithm number --print-number --description \"bar\" --pre-number 1234 --type post"
                ),
                Arguments.of(
                        new SnapperCmd("root", "post", "number", "bar", false, 1234, "important=yes"),
                        "snapper --config root create --cleanup-algorithm number --print-number --description \"bar\" --userdata \"important=yes\" --pre-number 1234 --type post"
                ),
                Arguments.of(
                        new SnapperCmd("root", "post", "number", "bar", false, 1234, "foo=bar,important=yes"),
                        "snapper --config root create --cleanup-algorithm number --print-number --description \"bar\" --userdata \"foo=bar,important=yes\" --pre-number 1234 --type post"
                ),
                Arguments.of(
                        new SnapperCmd("root", "post", "number", "bar", false, null, "foo=bar,important=yes"),
                        "snapper --config root create --cleanup-algorithm number --print-number --description \"bar\" --userdata \"foo=bar,important=yes\" --type single"
                )
        );
    }

    @ParameterizedTest
    @MethodSource("snapperCmdProvider")
    void testSnapperCmd(SnapperCmd snapperCmd, String actualCmd) {
        assertEquals(actualCmd, snapperCmd.toString());
    }

    @Test
    void testGetSnapperConfigs() throws IOException {
        Path path = Files.createTempFile("snapper", "conf");
        String data = "## Path: System/Snapper\n\n"
                + "## Type:        string\n"
                + "## Default:     \"\"\n"
                + "# List of snapper configurations.\n"
                + "SNAPPER_CONFIGS=\"home root foo bar\"\n";
        Files.write(path, data.getBytes());
        List<String> configs = Scripts.getSnapperConfigs(path);
        assertEquals(Arrays.asList("home", "root", "foo", "bar"), configs);
        Files.deleteIfExists(path);
    }

    @Test
    void testSkipSnapPac() {
        try {
            System.setProperty("SNAP_PAC_SKIP", "y");
            Map<String, String> env = new HashMap<>(System.getenv());
            env.put("SNAP_PAC_SKIP", "y");
            boolean result = Scripts.checkSkip(env);
            assertTrue(result);
        } finally {
            // No direct way to remove environment variables, so skip
        }
    }

    static Stream<Arguments> configProcessorCases() {
        return Stream.of(
                Arguments.of(
                        "root", "foo", List.of("bar"), "pre",
                        Map.of("description", "foo", "cleanup_algorithm", "number", "userdata", "", "snapshot", true)
                ),
                Arguments.of(
                        "root", "pacman -Syu", List.of(), "pre",
                        Map.of("description", "pacman -Syu", "cleanup_algorithm", "number", "userdata", "important=yes", "snapshot", true)
                ),
                Arguments.of(
                        "mail", "pacman -Syu", List.of(), "pre",
                        Map.of("description", "pacman -Syu", "cleanup_algorithm", "number", "userdata", "", "snapshot", false)
                ),
                Arguments.of(
                        "home", "pacman -Syu", List.of(), "pre",
                        Map.of("description", "pac", "cleanup_algorithm", "number", "userdata", "foo=bar,requestid=42", "snapshot", true)
                ),
                Arguments.of(
                        "home", "pacman -Syu", List.of(), "post",
                        Map.of("description", "a r", "cleanup_algorithm", "number", "userdata", "foo=bar,requestid=42", "snapshot", true)
                ),
                Arguments.of(
                        "myconfig", "pacman -S linux", List.of("linux"), "post",
                        Map.of("description", "linux", "cleanup_algorithm", "timeline",
                                "userdata", "foo=bar,important=yes,requestid=42", "snapshot", true)
                )
        );
    }

    @ParameterizedTest
    @MethodSource("configProcessorCases")
    void testConfigProcessor(String section, String command, List<String> packages, String snapshotType, Map<String, Object> result) throws IOException {
        Path config = Files.createTempFile("cfg", "ini");
        try (BufferedWriter writer = Files.newBufferedWriter(config)) {
            writer.write("[root]\n");
            writer.write("important_commands = [\"pacman -Syu\"]\n\n");
            writer.write("[home]\n");
            writer.write("snapshot = True\n");
            writer.write("desc_limit = 3\n");
            writer.write("post_description = a really long description\n");
            writer.write("userdata = [\"foo=bar\", \"requestid=42\"]\n\n");
            writer.write("[myconfig]\n");
            writer.write("snapshot = True\n");
            writer.write("cleanup_algorithm = timeline\n");
            writer.write("important_packages = [\"linux\", \"linux-lts\"]\n");
            writer.write("userdata = [\"foo=bar\", \"requestid=42\"]\n");
        }
        ConfigProcessor processor = new ConfigProcessor(config.toString(), snapshotType, command, packages);
        Map<String, Object> actual = processor.apply(section);
        assertEquals(result, actual);
        Files.deleteIfExists(config);
    }

    @Test
    void testPrefileReadNone() {
        Prefile prefile = new Prefile("root", "pre");
        assertNull(prefile.read());
    }

    @Test
    void testPrefileRead() {
        Prefile prefile = new Prefile("root", "pre");
        prefile.write("1234");
        Prefile postfile = new Prefile("root", "post");
        assertEquals("1234", postfile.read());
    }

    @Test
    void testNoPrefile() {
        Prefile prefile = new Prefile("foo-pre-file-not-found", "post");
        assertNull(prefile.read());
    }
}