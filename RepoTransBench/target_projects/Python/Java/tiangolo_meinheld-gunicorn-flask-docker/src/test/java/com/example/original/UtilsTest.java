package com.example.original;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicBoolean;
import static org.junit.jupiter.api.Assertions.*;

class UtilsTest {

    static class DummyContainer {
        Map<String, List<List<String>>> _top;
        DummyExecResult _execRunOut;
        byte[] _logsBytes;
        boolean _stopCalled = false;
        boolean _removeCalled = false;
        boolean _raiseOnTop;
        boolean _raiseOnExecRun;

        public DummyContainer() {
            this(null, null, null, true, false, false);
        }

        public DummyContainer(Map<String, List<List<String>>> top, DummyExecResult execRunOut, byte[] logsBytes,
                              boolean hasGunicorn, boolean raiseOnTop, boolean raiseOnExecRun) {
            if (!hasGunicorn) {
                List<String> proc = Arrays.asList("a", "b", "c", "d", "e", "f", "g", "python app.py");
                Map<String, List<List<String>>> _top = new HashMap<>();
                _top.put("Processes", Collections.singletonList(proc));
                this._top = _top;
            } else {
                List<String> proc = Arrays.asList("a", "b", "c", "d", "e", "f", "g", "gunicorn -c conf.py app:app");
                Map<String, List<List<String>>> _top = top != null ? top : new HashMap<>();
                if (top == null) {
                    _top.put("Processes", Collections.singletonList(proc));
                }
                this._top = _top;
            }
            this._execRunOut = execRunOut != null ? execRunOut :
                    new DummyExecResult("{\"key\": \"value\"}".getBytes());
            this._logsBytes = logsBytes != null ? logsBytes : "Some logs".getBytes();
            this._raiseOnTop = raiseOnTop;
            this._raiseOnExecRun = raiseOnExecRun;
        }

        public Map<String, List<List<String>>> top() {
            if (_raiseOnTop) throw new RuntimeException("Cannot get top of container");
            return _top;
        }

        public DummyExecResult exec_run(String cmd) {
            if (_raiseOnExecRun) throw new RuntimeException("exec_run failed");
            return _execRunOut;
        }

        public byte[] logs() {
            return _logsBytes;
        }

        public void stop() { _stopCalled = true; }

        public void remove() { _removeCalled = true; }
    }

    static class DummyExecResult {
        public byte[] output;

        public DummyExecResult(byte[] output) {
            this.output = output;
        }
    }

    static class DummyClient {
        Containers containers;

        static class Containers {
            DummyContainer container;
            boolean notfound;

            public Containers(DummyContainer container, boolean notfound) {
                this.container = container;
                this.notfound = notfound;
            }

            public DummyContainer get(String name) {
                if (notfound)
                    throw new DummyNotFoundException("not found");
                return container;
            }
        }

        public DummyClient(DummyContainer container, boolean notfound) {
            this.containers = new Containers(container, notfound);
        }
    }

    static class DummyNotFoundException extends RuntimeException {
        public DummyNotFoundException(String msg) { super(msg); }
    }

    // Equivalent of utils.get_process_names
    public List<String> getProcessNames(DummyContainer c) {
        List<List<String>> processes = c.top().get("Processes");
        List<String> processNames = new ArrayList<>();
        for (List<String> proc : processes) {
            String last = proc.get(proc.size() - 1);
            if (last.startsWith("gunicorn")) {
                processNames.add(last);
            }
        }
        return processNames;
    }

    // Equivalent of utils.get_gunicorn_conf_path
    public String getGunicornConfPath(DummyContainer c) {
        List<List<String>> processes = c.top().get("Processes");
        for (List<String> proc : processes) {
            String cmd = proc.get(proc.size() - 1);
            if (cmd.startsWith("gunicorn") && cmd.contains("-c")) {
                String[] parts = cmd.split(" ");
                for (int i = 0; i < parts.length; i++) {
                    if (parts[i].equals("-c") && i + 1 < parts.length) {
                        return parts[i + 1];
                    }
                }
            }
        }
        throw new IndexOutOfBoundsException("No gunicorn conf path found");
    }

    // Equivalent of utils.get_config (parses output of exec_run as JSON)
    public Map<String, Object> getConfig(DummyContainer c) {
        try {
            byte[] out = c.exec_run("cat conf.json").output;
            ObjectMapper mapper = new ObjectMapper();
            return mapper.readValue(out, Map.class);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    // Equivalent of utils.remove_previous_container
    public Void removePreviousContainer(DummyClient client) {
        try {
            DummyContainer c = client.containers.get("meinheld_flask_app");
            c.stop();
            c.remove();
            return null;
        } catch (DummyNotFoundException e) {
            return null;
        }
    }

    // Equivalent of utils.get_logs
    public String getLogs(DummyContainer c) {
        try {
            return new String(c.logs(), java.nio.charset.StandardCharsets.UTF_8);
        } catch (Exception e) {
            throw e;
        }
    }

    // Equivalent of utils.get_response_text1 (uses env)
    public String getResponseText1() {
        String version = System.getenv("PYTHON_VERSION");
        if (version == null) version = "unknown";
        return "Hello World from Flask in a Docker container running Python " + version +
                " with Meinheld and Gunicorn (default)";
    }

    @Test
    void test_get_process_names() {
        DummyContainer c = new DummyContainer();
        List<String> res = getProcessNames(c);
        assertTrue(res instanceof List);
        assertTrue(res.contains("gunicorn -c conf.py app:app"));
    }

    @Test
    void test_get_process_names_empty() {
        DummyContainer c = new DummyContainer(null, null, null, false, false, false);
        List<String> res = getProcessNames(c);
        assertTrue(res instanceof List);
        assertEquals(0, res.size());
    }

    @Test
    void test_get_gunicorn_conf_path() {
        DummyContainer c = new DummyContainer();
        String path = getGunicornConfPath(c);
        assertEquals("conf.py", path);
    }

    @Test
    void test_get_gunicorn_conf_path_no_gunicorn() {
        DummyContainer c = new DummyContainer(null, null, null, false, false, false);
        assertThrows(IndexOutOfBoundsException.class, () -> getGunicornConfPath(c));
    }

    @Test
    void test_get_config() {
        DummyExecResult dummyOut = new DummyExecResult("{\"foo\":42}".getBytes());
        DummyContainer c = new DummyContainer(null, dummyOut, null, true, false, false);
        Map<String, Object> config = getConfig(c);
        assertEquals(42, ((Number)config.get("foo")).intValue());
    }

    @Test
    void test_get_config_exec_run_error() {
        DummyContainer c = new DummyContainer(null, null, null, true, false, true);
        assertThrows(RuntimeException.class, () -> getConfig(c));
    }

    @Test
    void test_remove_previous_container_found() {
        DummyContainer c = new DummyContainer();
        DummyClient client = new DummyClient(c, false);
        removePreviousContainer(client);
        assertTrue(c._stopCalled);
        assertTrue(c._removeCalled);
    }

    @Test
    void test_remove_previous_container_notfound() {
        DummyClient client = new DummyClient(null, true);
        Void res = removePreviousContainer(client);
        assertNull(res);
    }

    @Test
    void test_get_logs() {
        DummyContainer c = new DummyContainer(null, null, "abc123".getBytes(), true, false, false);
        String logs = getLogs(c);
        assertEquals("abc123", logs);
    }

    @Test
    void test_get_response_text1() {
        Map<String, String> oldEnv = System.getenv();
        try {
            setEnv("PYTHON_VERSION", "3.9");
            String msg = getResponseText1();
            assertTrue(msg.contains("3.9"));
        } finally {
            // No easy way to restore env inside JVM; left as is for test
        }
    }

    @Test
    void test_get_logs_utf8_error() {
        DummyContainer c = new DummyContainer() {
            @Override
            public byte[] logs() {
                return new byte[]{(byte) 0xff};
            }
        };
        assertThrows(Exception.class, () -> getLogs(c));
    }

    // Utility to set a system environment variable for test (works for recent JVM/JDK)
    private static void setEnv(String key, String value) {
        try {
            Map<String, String> env = System.getenv();
            java.lang.reflect.Field field = env.getClass().getDeclaredField("m");
            field.setAccessible(true);
            ((Map<String, String>) field.get(env)).put(key, value);
        } catch (Exception e) {
            // do nothing or log warning
        }
    }
}