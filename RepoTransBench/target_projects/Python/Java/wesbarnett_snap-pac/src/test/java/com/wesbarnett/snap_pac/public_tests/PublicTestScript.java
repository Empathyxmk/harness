package com.wesbarnett.snap_pac.public_tests;

import com.wesbarnett.snap_pac.scripts.*;
import org.junit.jupiter.api.*;
import org.junit.jupiter.params.*;
import org.junit.jupiter.params.provider.*;
import java.nio.file.*;
import java.io.*;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicTestScript {

    static Stream<Arguments> snapperCmdProvider() {
        return Stream.of(
                Arguments.of(
                        new SnapperCmd("data", "pre", "timeline", "baz"),
                        "snapper --config data create --cleanup-algorithm timeline --print-number --description \"baz\" --type pre"
                ),
                Arguments.of(
                        new SnapperCmd("home", "post", "timeline", "qux", false, 4321),
                        "snapper --config home create --cleanup-algorithm timeline --print-number --description \"qux\" --pre-number 4321 --type post"
                ),
                Arguments.of(
                        new SnapperCmd("data", "post", "timeline", "quux", true, 5678),
                        "snapper --no-dbus --config data create --cleanup-algorithm timeline --print-number --description \"quux\" --pre-number 5678 --type post"
                ),
                Arguments.of(
                        new SnapperCmd("foo", "post", "timeline", "snap", false, 8765, "bar=foo"),
                        "snapper --config foo create --cleanup-algorithm timeline --print-number --description \"snap\" --userdata \"bar=foo\" --pre-number 8765 --type post"
                ),
                Arguments.of(
                        new SnapperCmd("home", "post", "timeline", "test", false, 2468, "alpha=beta,gamma=delta"),
                        "snapper --config home create --cleanup-algorithm timeline --print-number --description \"test\" --userdata \"alpha=beta,gamma=delta\" --pre-number 2468 --type post"
                ),
                Arguments.of(
                        new SnapperCmd("data", "post", "timeline", "snap", false, null, "foo=bar,baz=qux"),
                        "snapper --config data create --cleanup-algorithm timeline --print-number --description \"snap\" --userdata \"foo=bar,baz=qux\" --type single"
                )
        );
    }

    @ParameterizedTest
    @MethodSource("snapperCmdProvider")
    void testPublicSnapperCmd(SnapperCmd snapperCmd, String actualCmd) {
        assertEquals(actualCmd, snapperCmd.toString());
    }

    @Test
    void testPublicGetSnapperConfigs() throws IOException {
        Path p = Files.createTempFile("snapper", "conf");
        String data = "## Path: System/Snapper\n\n"
                + "## Type:        string\n"
                + "## Default:     \"\"\n"
                + "# List of snapper configurations.\n"
                + "SNAPPER_CONFIGS=\"data home alpha beta\"\n";
        Files.write(p, data.getBytes());
        List<String> configs = Scripts.getSnapperConfigs(p);
        assertEquals(Arrays.asList("data", "home", "alpha", "beta"), configs);
        Files.deleteIfExists(p);
    }

    @Test
    void testPublicSkipSnapPac() {
        Map<String, String> env = new HashMap<>(System.getenv());
        env.put("SNAP_PAC_SKIP", "yes");
        boolean result = Scripts.checkSkip(env);
        assertTrue(result);
    }

    static Stream<Arguments> configProcessorCases() {
        return Stream.of(
                Arguments.of(
                        "home", "bar", List.of("qux"), "pre",
                        Map.of("description", "bar", "cleanup_algorithm", "timeline", "userdata", "", "snapshot", true)
                ),
                Arguments.of(
                        "data", "apt-get update", List.of(), "pre",
                        Map.of("description", "apt-get update", "cleanup_algorithm", "timeline", "userdata", "critical=yes", "snapshot", true)
                ),
                Arguments.of(
                        "archive", "apt-get update", List.of(), "pre",
                        Map.of("description", "apt-get update", "cleanup_algorithm", "timeline", "userdata", "", "snapshot", false)
                ),
                Arguments.of(
                        "beta", "apt-get update", List.of(), "pre",
                        Map.of("description", "apt", "cleanup_algorithm", "timeline", "userdata", "foo=bar,requestid=99", "snapshot", true)
                ),
                Arguments.of(
                        "beta", "apt-get update", List.of(), "post",
                        Map.of("description", "test d", "cleanup_algorithm", "timeline", "userdata", "foo=bar,requestid=99", "snapshot", true)
                ),
                Arguments.of(
                        "special", "apt-get install kernel", List.of("kernel"), "post",
                        Map.of("description", "kernel", "cleanup_algorithm", "number",
                                "userdata", "foo=bar,critical=yes,requestid=99", "snapshot", true)
                )
        );
    }

    @ParameterizedTest
    @MethodSource("configProcessorCases")
    void testPublicConfigProcessor(String section, String command, List<String> packages, String snapshotType, Map<String, Object> result) throws IOException {
        Path config = Files.createTempFile("cfg", "ini");
        try (BufferedWriter writer = Files.newBufferedWriter(config)) {
            writer.write("[home]\n");
            writer.write("important_commands = [\"apt-get update\"]\n\n");
            writer.write("cleanup_algorithm = timeline\n");
            writer.write("[beta]\n");
            writer.write("snapshot = True\n");
            writer.write("desc_limit = 5\n");
            writer.write("post_description = test description for beta section\n");
            writer.write("userdata = [\"foo=bar\", \"requestid=99\"]\n\n");
            writer.write("[special]\n");
            writer.write("snapshot = True\n");
            writer.write("cleanup_algorithm = number\n");
            writer.write("important_packages = [\"kernel\", \"initrd\"]\n");
            writer.write("userdata = [\"foo=bar\", \"requestid=99\"]\n");
        }
        ConfigProcessor processor = new ConfigProcessor(config.toString(), snapshotType, command, packages);
        Map<String, Object> actual = processor.apply(section);
        assertEquals(result, actual);
        Files.deleteIfExists(config);
    }

    @Test
    void testPublicPrefileReadNone() {
        Prefile prefile = new Prefile("data", "pre");
        assertNull(prefile.read());
    }

    @Test
    void testPublicPrefileRead() {
        Prefile prefile = new Prefile("home", "pre");
        prefile.write("5678");
        Prefile postfile = new Prefile("home", "post");
        assertEquals("5678", postfile.read());
    }

    @Test
    void testPublicNoPrefile() {
        Prefile prefile = new Prefile("nonexistent-pre-file", "post");
        assertNull(prefile.read());
    }

}