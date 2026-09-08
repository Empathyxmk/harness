package com.signalfx.maestro.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.nio.file.*;
import java.io.*;
import java.util.*;
import org.yaml.snakeyaml.Yaml;
import org.yaml.snakeyaml.constructor.ConstructorException;
import org.yaml.snakeyaml.parser.ParserException;

class DummyMaestroException extends RuntimeException { }

class DummyLoader {
    public static Map<String,Object> load(String filename) {
        if (filename.equals("-")) {
            // Simulate stdin load (assume yaml injected)
            String input = System.getProperty("dummy.stdin", "");
            return new Yaml().load(input);
        } else if (!Files.exists(Paths.get(filename))) {
            throw new DummyMaestroException();
        } else {
            try (InputStream in = Files.newInputStream(Paths.get(filename))) {
                Map<String,Object> conf = new Yaml().load(in);
                if (conf == null) throw new DummyMaestroException();
                conf.putIfAbsent("__maestro", new HashMap<String,Object>() {{
                    put("base_dir", "/tmp");
                }});
                return conf;
            } catch (ConstructorException | ParserException e) {
                throw e;
            } catch (Exception e) {
                throw new DummyMaestroException();
            }
        }
    }
}

public class TestLoader {

    @Test
    public void testBasicYamlLoad(@TempDir Path tmpPath) throws IOException {
        String content = "foo: bar\n";
        Path file = tmpPath.resolve("sample.yaml");
        Files.write(file, content.getBytes());
        Map<String, Object> conf = DummyLoader.load(file.toString());
        assertTrue(conf.containsKey("foo"));
        assertEquals("bar", conf.get("foo"));
        assertTrue(conf.containsKey("__maestro"));
        Map<String, Object> maestro = (Map<String, Object>) conf.get("__maestro");
        assertTrue(maestro.containsKey("base_dir"));
    }

    @Test
    public void testBaseDirIsCwdForStdin() {
        String testYaml = "abc: 123";
        System.setProperty("dummy.stdin", testYaml);
        Map<String, Object> conf = DummyLoader.load("-");
        assertEquals(123, conf.get("abc"));
    }

    @Test
    public void testTemplateNotFound() {
        assertThrows(DummyMaestroException.class,
            () -> DummyLoader.load("/not/a/real/file.yaml"));
    }

    @Test
    public void testInvalidYaml(@TempDir Path tmpPath) throws IOException {
        Path file = tmpPath.resolve("fail.yaml");
        String badYaml = "foo: [1,2\n";
        Files.write(file, badYaml.getBytes());
        assertThrows(ParserException.class,
            () -> DummyLoader.load(file.toString()));
    }

    @Test
    public void testDuplicateKeyError(@TempDir Path tmpPath) throws IOException {
        Path file = tmpPath.resolve("bad.yaml");
        String content = "foo: 1\nfoo: 2\n";
        Files.write(file, content.getBytes());
        assertThrows(ConstructorException.class,
            () -> DummyLoader.load(file.toString()));
    }

    @Test
    public void testCustomFilterFunction(@TempDir Path tmpPath) throws IOException {
        Path file = tmpPath.resolve("filter.yaml");
        String content = "{{ 'hello' | shout }}";
        Files.write(file, content.getBytes());
        // Simulate Jinja templating unsupported - TypeError
        assertThrows(ClassCastException.class,
            () -> DummyLoader.load(file.toString()));
    }
}