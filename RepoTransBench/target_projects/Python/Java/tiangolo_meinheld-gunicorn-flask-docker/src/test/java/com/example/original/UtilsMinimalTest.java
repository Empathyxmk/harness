package com.example.original;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.*;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class UtilsMinimalTest {

    static class DummyContainer {
        Map<String, List<List<String>>> _top;
        DummyExecResult _execRunOut;
        byte[] _logsBytes;
        boolean _raiseOnTop = false;
        boolean _raiseOnExecRun = false;
        boolean _stopCalled = false;
        boolean _removeCalled = false;

        public DummyContainer() {
            this("logdata".getBytes(), false, false);
        }

        public DummyContainer(byte[] logsBytes, boolean raiseOnTop, boolean raiseOnExecRun) {
            this._top = new HashMap<>();
            this._top.put("Processes", Arrays.asList(
                    Arrays.asList("a", "b", "c", "d", "e", "f", "g", "gunicorn -c conf.py app:app")
            ));
            this._execRunOut = new DummyExecResult("{\"newkey\": \"newvalue\"}".getBytes());
            this._logsBytes = logsBytes;
            this._raiseOnTop = raiseOnTop;
            this._raiseOnExecRun = raiseOnExecRun;
        }

        public Map<String, List<List<String>>> top() {
            if (_raiseOnTop) throw new RuntimeException("Simulate top error");
            return _top;
        }

        public DummyExecResult exec_run(String cmd) {
            if (_raiseOnExecRun) throw new RuntimeException("Simulate exec_run error");
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
        public DummyExecResult(byte[] output) { this.output = output; }
    }

    // wait_for_gunicorn (simulate sleep/timeout logic)
    public boolean waitForGunicorn(DummyContainer c, double sleepTime, double timeout) {
        long limit = System.nanoTime() + (long)(timeout * 1e9);
        while (System.nanoTime() < limit) {
            try {
                List<List<String>> ps = c.top().get("Processes");
                for (List<String> proc : ps) {
                    String last = proc.get(proc.size() - 1);
                    if (last.startsWith("gunicorn")) return true;
                }
            } catch (Exception e) { return false; }
            try { Thread.sleep((long)(sleepTime * 1000)); } catch (InterruptedException ignored) {}
        }
        return false;
    }

    // get_config_from_container
    public Map<String, Object> getConfigFromContainer(DummyContainer c, String path) {
        try {
            byte[] out = c.exec_run("cat " + path).output;
            ObjectMapper mapper = new ObjectMapper();
            return mapper.readValue(out, Map.class);
        } catch (Exception e) {
            return null;
        }
    }

    // print_container_logs (just returns String for assert)
    public String printContainerLogs(DummyContainer c) {
        String logs = new String(c.logs(), java.nio.charset.StandardCharsets.UTF_8);
        String output = "Container logs:\n" + logs;
        System.out.print(output);
        return output;
    }

    // cleanup_container
    public void cleanupContainer(DummyContainer c) {
        c.stop();
        c.remove();
    }

    @Test
    void test_wait_for_gunicorn_gunicorn_found() {
        DummyContainer c = new DummyContainer();
        boolean result = waitForGunicorn(c, 0.01, 0.05);
        assertTrue(result);
    }

    @Test
    void test_wait_for_gunicorn_gunicorn_notfound() {
        DummyContainer c = new DummyContainer();
        c._top = new HashMap<>();
        c._top.put("Processes", Arrays.asList(
                Arrays.asList("python app.py")
        ));
        boolean result = waitForGunicorn(c, 0.01, 0.03);
        assertFalse(result);
    }

    @Test
    void test_get_config_from_container_success() {
        DummyContainer c = new DummyContainer();
        Map<String, Object> r = getConfigFromContainer(c, "/etc/config.json");
        assertTrue(r.containsKey("newkey"));
    }

    @Test
    void test_get_config_from_container_exec_run_fail() {
        DummyContainer c = new DummyContainer("logdata".getBytes(), false, true);
        Map<String, Object> r = getConfigFromContainer(c, "/fakepath");
        assertNull(r);
    }

    @Test
    void test_print_container_logs_prints() {
        DummyContainer c = new DummyContainer();
        String result = printContainerLogs(c);
        assertTrue(result.contains("Container logs:"));
    }

    @Test
    void test_cleanup_container_calls_methods() {
        DummyContainer c = new DummyContainer();
        cleanupContainer(c);
        assertTrue(c._stopCalled);
        assertTrue(c._removeCalled);
    }
}