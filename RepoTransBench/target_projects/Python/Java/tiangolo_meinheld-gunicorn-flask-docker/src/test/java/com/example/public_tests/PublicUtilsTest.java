package com.example.public_tests;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicUtilsTest {

    static class DummyContainer {
        Map<String, List<List<String>>> _top;
        DummyExecResult _execRunOut;
        byte[] _logsBytes;
        boolean _stopCalled = false;
        boolean _removeCalled = false;
        boolean _raiseOnTop;
        boolean _raiseOnExecRun;

        public DummyContainer() { this(null, null, null, true, false, false); }

        public DummyContainer(Map<String,List<List<String>>> top, DummyExecResult execRunOut, byte[] logsBytes,
                              boolean hasGunicorn, boolean raiseOnTop, boolean raiseOnExecRun) {
            if (!hasGunicorn) {
                List<String> proc = Arrays.asList("z", "y", "x", "w", "v", "u", "t", "python manage.py");
                Map<String, List<List<String>>> _top = new HashMap<>();
                _top.put("Processes", Collections.singletonList(proc));
                this._top = _top;
            } else {
                List<String> proc = Arrays.asList("1", "2", "3", "4", "5", "6", "7", "gunicorn -w 3 -b :5000 anotherapp:app");
                Map<String, List<List<String>>> _top = top != null ? top : new HashMap<>();
                if (top == null) {
                    _top.put("Processes", Collections.singletonList(proc));
                }
                this._top = _top;
            }
            this._execRunOut = execRunOut != null ? execRunOut :
                    new DummyExecResult("{\"bar\": 43}".getBytes());
            this._logsBytes = logsBytes != null ? logsBytes : "Different logs".getBytes();
            this._raiseOnTop = raiseOnTop;
            this._raiseOnExecRun = raiseOnExecRun;
        }

        public Map<String,List<List<String>>> top() {
            if (_raiseOnTop)
                throw new RuntimeException("Top method failed for container");
            return _top;
        }

        public DummyExecResult exec_run(String cmd) {
            if (_raiseOnExecRun)
                throw new RuntimeException("exec_run simulated failure");
            return _execRunOut;
        }

        public byte[] logs() { return _logsBytes; }

        public void stop() { _stopCalled = true; }
        public void remove() { _removeCalled = true; }
    }

    static class DummyExecResult {
        public byte[] output;
        public DummyExecResult(byte[] output) { this.output = output; }
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
                    throw new DummyNotFoundException("container not present");
                return container;
            }
        }
        public DummyClient(DummyContainer container, boolean notfound) {
            containers = new Containers(container, notfound);
        }
    }
    static class DummyNotFoundException extends RuntimeException {
        public DummyNotFoundException(String msg) { super(msg); }
    }

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
        throw new IndexOutOfBoundsException("no gunicorn conf path found");
    }

    public Map<String, Object> getConfig(DummyContainer c) {
        try {
            byte[] out = c.exec_run("cat conf.json").output;
            ObjectMapper mapper = new ObjectMapper();
            return mapper.readValue(out, Map.class);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

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

    public String getLogs(DummyContainer c) {
        try {
            return new String(c.logs(), java.nio.charset.StandardCharsets.UTF_8);
        } catch (Exception e) {
            throw e;
        }
    }

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
        assertTrue(res.contains("gunicorn -w 3 -b :5000 anotherapp:app"));
    }

    @Test
    void test_get_process_names_empty() {
        DummyContainer c = new DummyContainer(null, null, null, false, false, false);
        List<String> res = getProcessNames(c);
        assertTrue(res instanceof List);
        assertTrue(res.isEmpty());
    }

    @Test
    void test_get_gunicorn_conf_path() {
        Map<String, List<List<String>>> top = new HashMap<>();
        top.put("Processes", Arrays.asList(
                Arrays.asList("1", "2", "3", "4", "5", "6", "7", "gunicorn -c custom_conf.py anotherapp:app")
        ));
        DummyContainer c = new DummyContainer(top, null, null, true, false, false);
        String path = getGunicornConfPath(c);
        assertEquals("custom_conf.py", path);
    }

    @Test
    void test_get_gunicorn_conf_path_no_gunicorn() {
        DummyContainer c = new DummyContainer(null, null, null, false, false, false);
        assertThrows(IndexOutOfBoundsException.class, () -> getGunicornConfPath(c));
    }

    @Test
    void test_get_config() {
        DummyExecResult dummyOut = new DummyExecResult("{\"baz\":99}".getBytes());
        DummyContainer c = new DummyContainer(null, dummyOut, null, true, false, false);
        Map<String,Object> config = getConfig(c);
        assertEquals(99, ((Number)config.get("baz")).intValue());
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
        DummyContainer c = new DummyContainer(null, null, "xyz789".getBytes(), true, false, false);
        String logs = getLogs(c);
        assertEquals("xyz789", logs);
    }

    @Test
    void test_get_response_text1() {
        setEnv("PYTHON_VERSION", "3.10");
        String msg = getResponseText1();
        assertTrue(msg.contains("3.10"));
    }

    @Test
    void test_get_logs_utf8_error() {
        DummyContainer c = new DummyContainer() {
            @Override
            public byte[] logs() { return new byte[]{(byte)0xfe}; }
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
        }
    }
}