package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.function.Executable;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.Arguments;

import static org.junit.jupiter.api.Assertions.*;

import java.util.*;
import java.util.stream.Stream;

// NOTE: This test assumes the existence of HonchoEnviron along with the static methods `parse`, `parseProcfile`, `expandProcesses`, and class `Procfile`.
// You will need to implement similar classes/methods in your main Honcho Java code.

class TestEnviron {
    // PARAMETERIZED TESTS for env parsing

    static Stream<Arguments> provideEnvContents() {
        return Stream.of(
            Arguments.of("FOO=bar\n", Map.of("FOO", "bar")),
            Arguments.of("FOO=bar\nBAZ=qux\n", Map.of("FOO", "bar", "BAZ", "qux")),
            Arguments.of("FOO=bar", Map.of("FOO", "bar")),
            Arguments.of("#commented: command\n", Collections.emptyMap()),
            Arguments.of("-foo=command\n", Collections.emptyMap()),
            Arguments.of("MYVAR='hello\"world'\n", Map.of("MYVAR", "hello\"world")),
            Arguments.of("MYVAR=\"hello'world\"\n", Map.of("MYVAR", "hello'world")),
            Arguments.of("MYVAR='\"surrounded\"'\n", Map.of("MYVAR", "\"surrounded\"")),
            Arguments.of("MYVAR=\\\"escaped\\\"\n", Map.of("MYVAR", "\"escaped\"")),
            Arguments.of("MYVAR=user@domain.com\n", Map.of("MYVAR", "user@domain.com")),
            Arguments.of("MYVAR=~pun|u@|0n$=\n", Map.of("MYVAR", "~pun|u@|0n$=")),
            Arguments.of("MYVAR=⋃ñᴉ—☪ó∂ǝ\n", Map.of("MYVAR", "⋃ñᴉ—☪ó∂ǝ")),
            Arguments.of("ṀẎṾẠṚ=value\n", Collections.emptyMap()),
            Arguments.of("MYVAR='sp ace'\n", Map.of("MYVAR", "sp ace")),
            Arguments.of(
                "TABS='foo\\tbar'\nNEWLINES='foo\\nbar'\nDOLLAR='foo\\\\$bar'\n",
                Map.of("TABS", "foo\\tbar", "NEWLINES", "foo\\nbar", "DOLLAR", "foo\\$bar")
            )
        );
    }

    @ParameterizedTest
    @MethodSource("provideEnvContents")
    void testEnvironParse(String content, Map<String, String> expected) {
        Map<String, String> result = HonchoEnviron.parse(content);
        assertEquals(expected, result);
    }

    static Stream<Arguments> provideProcfileContents() {
        return Stream.of(
            Arguments.of("web: command\n", Map.of("web", "command")),
            Arguments.of("foo: python foo.py\nbar: python bar.py\n", Map.of("foo", "python foo.py", "bar", "python bar.py")),
            Arguments.of("web: command", Map.of("web", "command")),
            Arguments.of("#commented: command\n", Collections.emptyMap()),
            Arguments.of("+foo: command\n", Collections.emptyMap()),
            Arguments.of("-foo_bar: command\n", Map.of("-foo_bar", "command")),
            Arguments.of("web: sh -c \"echo $FOOBAR\" >/dev/null 2>&1\n", Map.of("web", "sh -c \"echo $FOOBAR\" >/dev/null 2>&1"))
        );
    }

    @ParameterizedTest
    @MethodSource("provideProcfileContents")
    void testParseProcfile(String content, Map<String, String> expected) {
        HonchoEnviron.Procfile p = HonchoEnviron.parseProcfile(content);
        assertEquals(expected, p.processes);
    }

    @Test
    void testParseProcfileOrdered() {
        String content = "one: onecommand\ntwo: twocommand\nthree: twocommand\nfour: fourcommand\n";
        HonchoEnviron.Procfile p = HonchoEnviron.parseProcfile(content);
        List<String> order = new ArrayList<>(p.processes.keySet());
        assertEquals(List.of("one", "two", "three", "four"), order);
    }

    @Nested
    class ProcfileClassTests {
        @Test
        void testHasNoProcessesAfterInit() {
            HonchoEnviron.Procfile p = new HonchoEnviron.Procfile();
            assertEquals(0, p.processes.size());
        }
        @Test
        void testAddProcess() {
            HonchoEnviron.Procfile p = new HonchoEnviron.Procfile();
            p.addProcess("foo", "echo 123");
            assertEquals("echo 123", p.processes.get("foo"));
        }
        @Test
        void testAddProcessEnsuresUniqueName() {
            HonchoEnviron.Procfile p = new HonchoEnviron.Procfile();
            p.addProcess("foo", "echo 123");
            assertThrows(AssertionError.class, () -> p.addProcess("foo", "echo 123"));
        }
    }

    // Helper for expandProcesses expansion (mimics ep() in Python)
    static List<HonchoEnviron.ProcessAssignment> ep(Object[]... argsAndKwargs) {
        // This helper builds an ordered process map and passes on kwargs
        LinkedHashMap<String, String> processMap = new LinkedHashMap<>();
        Map<String, Object> kwargs = new HashMap<>();
        for (Object[] arr : argsAndKwargs) {
            if (arr.length == 2 && arr[0] instanceof String && arr[1] instanceof String) {
                processMap.put((String) arr[0], (String) arr[1]);
            } else if (arr.length == 1 && arr[0] instanceof Map) {
                kwargs.putAll((Map<String, Object>) arr[0]);
            }
        }
        return HonchoEnviron.expandProcesses(processMap, kwargs);
    }

    @Test
    void testExpandProcessesName() {
        List<HonchoEnviron.ProcessAssignment> p = ep(new Object[]{"foo", "some command"});
        assertEquals(1, p.size());
        assertEquals("foo.1", p.get(0).name);
    }

    @Test
    void testExpandProcessesNameMultiple() {
        List<HonchoEnviron.ProcessAssignment> p = ep(
            new Object[]{"foo", "some command"},
            new Object[]{"bar", "another command"}
        );
        assertEquals(2, p.size());
        assertEquals("foo.1", p.get(0).name);
        assertEquals("bar.1", p.get(1).name);
    }

    @Test
    void testExpandProcessesNameConcurrency() {
        Map<String, Object> concurrency = Map.of("foo", 3);
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command")),
            Map.of("concurrency", concurrency)
        );
        assertEquals(3, p.size());
        assertEquals("foo.1", p.get(0).name);
        assertEquals("foo.2", p.get(1).name);
        assertEquals("foo.3", p.get(2).name);
    }

    @Test
    void testExpandProcessesNameConcurrencyMultiple() {
        Map<String, Object> concurrency = Map.of("foo", 3, "bar", 2);
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command", "bar", "another command")),
            Map.of("concurrency", concurrency)
        );
        assertEquals(5, p.size());
        assertEquals("foo.1", p.get(0).name);
        assertEquals("foo.2", p.get(1).name);
        assertEquals("foo.3", p.get(2).name);
        assertEquals("bar.1", p.get(3).name);
        assertEquals("bar.2", p.get(4).name);
    }

    @Test
    void testExpandProcessesCommand() {
        List<HonchoEnviron.ProcessAssignment> p = ep(new Object[]{"foo", "some command"});
        assertEquals("some command", p.get(0).cmd);
    }

    @Test
    void testExpandProcessesPortNotDefaulted() {
        List<HonchoEnviron.ProcessAssignment> p = ep(new Object[]{"foo", "some command"});
        assertFalse(p.get(0).env.containsKey("PORT"));
    }

    @Test
    void testExpandProcessesPort() {
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command")),
            Map.of("port", 8000)
        );
        assertEquals("8000", p.get(0).env.get("PORT"));
    }

    @Test
    void testExpandProcessesPortMultiple() {
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command", "bar", "another command")),
            Map.of("port", 8000)
        );
        assertEquals("8000", p.get(0).env.get("PORT"));
        assertEquals("8100", p.get(1).env.get("PORT"));
    }

    @Test
    void testExpandProcessesPortFromEnv() {
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command", "bar", "another command")),
            Map.of("env", Map.of("PORT", 8000))
        );
        assertEquals("8000", p.get(0).env.get("PORT"));
        assertEquals("8100", p.get(1).env.get("PORT"));
    }

    @Test
    void testExpandProcessesPortFromEnvCoercedToNumber() {
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command")),
            Map.of("env", Map.of("PORT", "5000"))
        );
        assertEquals("5000", p.get(0).env.get("PORT"));
    }

    @Test
    void testExpandProcessesPortFromEnvOverrides() {
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command")),
            Map.of("env", Map.of("PORT", 5000), "port", 8000)
        );
        assertEquals("5000", p.get(0).env.get("PORT"));
    }

    @Test
    void testExpandProcessesPortConcurrency() {
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command", "bar", "another command")),
            Map.of("concurrency", Map.of("foo", 3, "bar", 2), "port", 4000)
        );
        assertEquals("4000", p.get(0).env.get("PORT"));
        assertEquals("4001", p.get(1).env.get("PORT"));
        assertEquals("4002", p.get(2).env.get("PORT"));
        assertEquals("4100", p.get(3).env.get("PORT"));
        assertEquals("4101", p.get(4).env.get("PORT"));
    }

    @Test
    void testExpandProcessesQuiet() {
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command")),
            Map.of("quiet", List.of("foo", "bar"))
        );
        assertTrue(p.get(0).quiet);
    }

    @Test
    void testExpandProcessesQuietMultiple() {
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command", "bar", "another command")),
            Map.of("quiet", List.of("foo"))
        );
        assertTrue(p.get(0).quiet);
        assertFalse(p.get(1).quiet);
    }

    @Test
    void testExpandProcessesEnv() {
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command")),
            Map.of("env", Map.of("ANIMAL", "giraffe", "DEBUG", "false"))
        );
        assertEquals("giraffe", p.get(0).env.get("ANIMAL"));
        assertEquals("false", p.get(0).env.get("DEBUG"));
    }

    @Test
    void testExpandProcessesEnvMultiple() {
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command", "bar", "another command")),
            Map.of("env", Map.of("ANIMAL", "giraffe", "DEBUG", "false"))
        );
        assertEquals("giraffe", p.get(0).env.get("ANIMAL"));
        assertEquals("false", p.get(0).env.get("DEBUG"));
        assertEquals("giraffe", p.get(1).env.get("ANIMAL"));
        assertEquals("false", p.get(1).env.get("DEBUG"));
    }

    @Test
    void testSetEnvProcessName() {
        List<HonchoEnviron.ProcessAssignment> p = HonchoEnviron.expandProcesses(
            new LinkedHashMap<>(Map.of("foo", "some command", "bar", "another command")),
            Map.of("concurrency", Map.of("foo", 3, "bar", 2))
        );
        assertEquals("foo.1", p.get(0).env.get("HONCHO_PROCESS_NAME"));
        assertEquals("foo.2", p.get(1).env.get("HONCHO_PROCESS_NAME"));
        assertEquals("foo.3", p.get(2).env.get("HONCHO_PROCESS_NAME"));
        assertEquals("bar.1", p.get(3).env.get("HONCHO_PROCESS_NAME"));
        assertEquals("bar.2", p.get(4).env.get("HONCHO_PROCESS_NAME"));
    }
}